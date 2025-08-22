from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.vehicles import Vehicle
from app.schemas.vehicles import VehicleSearch

def get_vehicle_by_plate(db: Session, plate_number: str) -> Optional[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.plate_number == plate_number.upper()).first()

def get_vehicles_by_owner(db: Session, owner_id: int) -> List[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.owner_id == owner_id).all()

def search_vehicles(db: Session, search_params: VehicleSearch) -> List[Vehicle]:
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

def get_vehicles_by_color(db: Session, color: str) -> List[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.color.ilike(f"%{color}%")).all()

def get_vehicles_by_make(db: Session, make: str) -> List[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.make.ilike(f"%{make}%")).all()

def get_vehicles_by_type(db: Session, vehicle_type: str) -> List[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.vehicle_type == vehicle_type).all()

def get_large_vehicles(db: Session) -> List[Vehicle]:
    return db.query(Vehicle).filter(Vehicle.vehicle_type.in_(["Large", "SUV"])).all()