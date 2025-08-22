from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException
from models.parking_slots import ParkingSlot
from schemas.parking_slots import ParkingSlotCreate, ParkingSlotUpdate

def create_parking_slot(db: Session, payload: ParkingSlotCreate) -> ParkingSlot:
    obj_data = payload.model_dump()
    
    if obj_data.get("slot_number"):
        obj_data["slot_number"] = obj_data["slot_number"].upper()
    if obj_data.get("row_identifier"):
        obj_data["row_identifier"] = obj_data["row_identifier"].upper()
    
    slot = ParkingSlot(**obj_data)
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot

def get_parking_slot(db: Session, slot_id: int) -> ParkingSlot:
    slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    return slot

def get_available_slots(db: Session, skip: int = 0, limit: int = 100) -> List[ParkingSlot]:
    return db.query(ParkingSlot).filter(
        ParkingSlot.is_occupied == False
    ).offset(skip).limit(limit).all()

def get_handicap_accessible_slots(db: Session, lot_id: Optional[int] = None) -> List[ParkingSlot]:
    query = db.query(ParkingSlot).filter(ParkingSlot.is_handicap_accessible == True)
    if lot_id:
        query = query.filter(ParkingSlot.lot_id == lot_id)
    return query.order_by(ParkingSlot.distance_from_exit).all()

def get_large_slots(db: Session, lot_id: Optional[int] = None) -> List[ParkingSlot]:
    query = db.query(ParkingSlot).filter(ParkingSlot.slot_size == "large")
    if lot_id:
        query = query.filter(ParkingSlot.lot_id == lot_id)
    return query.filter(ParkingSlot.is_occupied == False).all()

def update_parking_slot(db: Session, slot_id: int, payload: ParkingSlotUpdate) -> ParkingSlot:
    slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "slot_number" and value:
            value = value.upper()
        elif field == "row_identifier" and value:
            value = value.upper()
        setattr(slot, field, value)
    
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot