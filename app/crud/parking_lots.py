from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.parking_lots import ParkingLot
from app.schemas.parking_lots import ParkingLotCreate, ParkingLotUpdate


class ParkingLotCRUD:
    def create(self, db: Session, obj_in: ParkingLotCreate) -> ParkingLot:
        db_obj = ParkingLot(
            name=obj_in.name,
            address=obj_in.address,
            total_capacity=obj_in.total_capacity,
            available_slots=obj_in.available_slots,
            is_full=obj_in.is_full,
            owner_name=obj_in.owner_name
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[ParkingLot]:
        return db.query(ParkingLot).filter(ParkingLot.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ParkingLot]:
        return db.query(ParkingLot).offset(skip).limit(limit).all()

    def get_by_name(self, db: Session, name: str) -> Optional[ParkingLot]:
        return db.query(ParkingLot).filter(ParkingLot.name == name).first()

    def get_available(self, db: Session) -> List[ParkingLot]:
        return db.query(ParkingLot).filter(ParkingLot.available_slots > 0).all()

    def get_full_lots(self, db: Session) -> List[ParkingLot]:
        return db.query(ParkingLot).filter(ParkingLot.is_full == True).all()

    def get_by_owner(self, db: Session, owner_name: str) -> List[ParkingLot]:
        return db.query(ParkingLot).filter(ParkingLot.owner_name == owner_name).all()

    def update_capacity(self, db: Session, lot_id: int, change: int) -> ParkingLot:
        lot = self.get(db, lot_id)
        if lot:
            lot.available_slots += change
            if lot.available_slots <= 0:
                lot.available_slots = 0
                lot.is_full = True
            elif lot.available_slots > 0:
                lot.is_full = False
            
            db.add(lot)
            db.commit()
            db.refresh(lot)
        return lot

    def decrease_capacity(self, db: Session, lot_id: int) -> ParkingLot:
        return self.update_capacity(db, lot_id, -1)

    def increase_capacity(self, db: Session, lot_id: int) -> ParkingLot:
        return self.update_capacity(db, lot_id, 1)

    def update(self, db: Session, *, db_obj: ParkingLot, obj_in: ParkingLotUpdate) -> ParkingLot:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        if "available_slots" in update_data or "total_capacity" in update_data:
            db_obj.is_full = db_obj.available_slots <= 0
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ParkingLot:
        obj = db.query(ParkingLot).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def count(self, db: Session) -> int:
        return db.query(ParkingLot).count()


parking_lot_crud = ParkingLotCRUD()