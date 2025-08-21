from sqlalchemy.orm import Session
from typing import List, Optional
from models.vehicles import Vehicle
from schemas.vehicles import VehicleCreate, VehicleUpdate, VehicleSearch

class VehicleCRUD:
    def create(self, db: Session, obj_in: VehicleCreate) -> Vehicle:
        """Create a new vehicle."""
        db_obj = Vehicle(
            plate_number=obj_in.plate_number.upper(),
            make=obj_in.make,
            model=obj_in.model,
            color=obj_in.color,
            vehicle_type=obj_in.vehicle_type,
            owner_id=obj_in.owner_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[Vehicle]:
        """Get vehicle by ID."""
        return db.query(Vehicle).filter(Vehicle.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        """Get multiple vehicles with pagination."""
        return db.query(Vehicle).offset(skip).limit(limit).all()

    def get_by_plate(self, db: Session, plate_number: str) -> Optional[Vehicle]:
        """Get vehicle by plate number."""
        return db.query(Vehicle).filter(Vehicle.plate_number == plate_number.upper()).first()

    def get_by_owner(self, db: Session, owner_id: int) -> List[Vehicle]:
        """Get all vehicles owned by a driver."""
        return db.query(Vehicle).filter(Vehicle.owner_id == owner_id).all()

    def search(self, db: Session, search_params: VehicleSearch) -> List[Vehicle]:
        """Search vehicles by multiple criteria (UC12-UC16)."""
        query = db.query(Vehicle)
        
        if search_params.plate_number:
            query = query.filter(Vehicle.plate_number.ilike(f"%{search_params.plate_number}%"))
        
        if search_params.make:
            query = query.filter(Vehicle.make.ilike(f"%{search_params.make}%"))
        
        if search_params.color:
            query = query.filter(Vehicle.color.ilike(f"%{search_params.color}%"))
        
        if search_params.vehicle_type:
            query = query.filter(Vehicle.vehicle_type == search_params.vehicle_type)
        
        return query.all()

    def get_by_color(self, db: Session, color: str) -> List[Vehicle]:
        """Get vehicles by color (UC12)."""
        return db.query(Vehicle).filter(Vehicle.color.ilike(f"%{color}%")).all()

    def get_by_make(self, db: Session, make: str) -> List[Vehicle]:
        """Get vehicles by make (UC13)."""
        return db.query(Vehicle).filter(Vehicle.make.ilike(f"%{make}%")).all()

    def get_by_type(self, db: Session, vehicle_type: str) -> List[Vehicle]:
        """Get vehicles by type (UC14)."""
        return db.query(Vehicle).filter(Vehicle.vehicle_type == vehicle_type).all()

    def get_large_vehicles(self, db: Session) -> List[Vehicle]:
        """Get large vehicles and SUVs (UC11)."""
        return db.query(Vehicle).filter(Vehicle.vehicle_type.in_(["Large", "SUV"])).all()

    def update(self, db: Session, *, db_obj: Vehicle, obj_in: VehicleUpdate) -> Vehicle:
        """Update vehicle information."""
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "plate_number" and value:
                value = value.upper()
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Vehicle:
        """Delete vehicle by ID."""
        obj = db.query(Vehicle).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def count(self, db: Session) -> int:
        """Count total vehicles."""
        return db.query(Vehicle).count()

vehicle_crud = VehicleCRUD()