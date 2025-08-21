from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.parking_slots import ParkingSlot
from app.schemas.parking_slots import ParkingSlotCreate, ParkingSlotUpdate


class ParkingSlotCRUD:
    def create(self, db: Session, obj_in: ParkingSlotCreate) -> ParkingSlot:
        db_obj = ParkingSlot(
            slot_number=obj_in.slot_number.upper(),
            lot_id=obj_in.lot_id,
            row_identifier=obj_in.row_identifier.upper(),
            is_occupied=obj_in.is_occupied,
            is_handicap_accessible=obj_in.is_handicap_accessible,
            distance_from_exit=obj_in.distance_from_exit,
            slot_size=obj_in.slot_size
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[ParkingSlot]:
        return db.query(ParkingSlot).filter(ParkingSlot.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ParkingSlot]:
        return db.query(ParkingSlot).offset(skip).limit(limit).all()

    def get_by_slot_and_lot(self, db: Session, slot_number: str, lot_id: int) -> Optional[ParkingSlot]:
        return db.query(ParkingSlot).filter(
            ParkingSlot.slot_number == slot_number.upper(),
            ParkingSlot.lot_id == lot_id
        ).first()

    def get_by_lot(self, db: Session, lot_id: int, *, skip: int = 0, limit: int = 100) -> List[ParkingSlot]:
        return db.query(ParkingSlot).filter(
            ParkingSlot.lot_id == lot_id
        ).offset(skip).limit(limit).all()

    def get_available(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ParkingSlot]:
        return db.query(ParkingSlot).filter(
            ParkingSlot.is_occupied == False
        ).offset(skip).limit(limit).all()

    def get_available_by_lot(self, db: Session, lot_id: int, *, skip: int = 0, limit: int = 100) -> List[ParkingSlot]:
        return db.query(ParkingSlot).filter(
            ParkingSlot.lot_id == lot_id,
            ParkingSlot.is_occupied == False
        ).offset(skip).limit(limit).all()

    def get_handicap_accessible(self, db: Session, lot_id: Optional[int] = None) -> List[ParkingSlot]:
        query = db.query(ParkingSlot).filter(ParkingSlot.is_handicap_accessible == True)
        if lot_id:
            query = query.filter(ParkingSlot.lot_id == lot_id)
        return query.order_by(ParkingSlot.distance_from_exit).all()

    def get_large_slots(self, db: Session, lot_id: Optional[int] = None) -> List[ParkingSlot]:
        query = db.query(ParkingSlot).filter(ParkingSlot.slot_size == "large")
        if lot_id:
            query = query.filter(ParkingSlot.lot_id == lot_id)
        return query.filter(ParkingSlot.is_occupied == False).all()

    def get_by_row(self, db: Session, row_identifier: str, lot_id: Optional[int] = None) -> List[ParkingSlot]:
        query = db.query(ParkingSlot).filter(ParkingSlot.row_identifier == row_identifier.upper())
        if lot_id:
            query = query.filter(ParkingSlot.lot_id == lot_id)
        return query.all()

    def occupy_slot(self, db: Session, slot_id: int) -> ParkingSlot:
        slot = self.get(db, slot_id)
        if slot:
            slot.is_occupied = True
            db.add(slot)
            db.commit()
            db.refresh(slot)
        return slot

    def free_slot(self, db: Session, slot_id: int) -> ParkingSlot:
        slot = self.get(db, slot_id)
        if slot:
            slot.is_occupied = False
            db.add(slot)
            db.commit()
            db.refresh(slot)
        return slot

    def get_best_slot_for_handicap(self, db: Session, lot_id: int) -> Optional[ParkingSlot]:
        return db.query(ParkingSlot).filter(
            ParkingSlot.lot_id == lot_id,
            ParkingSlot.is_handicap_accessible == True,
            ParkingSlot.is_occupied == False
        ).order_by(ParkingSlot.distance_from_exit).first()

    def update(self, db: Session, *, db_obj: ParkingSlot, obj_in: ParkingSlotUpdate) -> ParkingSlot:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "slot_number" and value:
                value = value.upper()
            elif field == "row_identifier" and value:
                value = value.upper()
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ParkingSlot:
        obj = db.query(ParkingSlot).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def count(self, db: Session) -> int:
        return db.query(ParkingSlot).count()


parking_slot_crud = ParkingSlotCRUD()