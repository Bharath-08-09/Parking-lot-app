from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.schemas.parking_slots import ParkingSlotCreate, ParkingSlotUpdate, ParkingSlotResponse, ParkingSlotList, SlotSize
from app.crud.parking_slots import parking_slot_crud
from app.crud.parking_lots import parking_lot_crud


router = APIRouter(prefix="/parking-slots", tags=["parking-slots"])


@router.post("/", response_model=ParkingSlotResponse, status_code=status.HTTP_201_CREATED)
def create_parking_slot(slot: ParkingSlotCreate, db: Session = Depends(get_db)):
    if not parking_lot_crud.get(db, slot.lot_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parking lot not found"
        )
    
    if parking_slot_crud.get_by_slot_and_lot(db, slot.slot_number, slot.lot_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot number already exists in this lot"
        )
    
    return parking_slot_crud.create(db, slot)


@router.get("/", response_model=ParkingSlotList)
def get_parking_slots(
    skip: int = 0, 
    limit: int = 100,
    lot_id: Optional[int] = Query(None),
    available_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    if lot_id:
        if available_only:
            slots = parking_slot_crud.get_available_by_lot(db, lot_id, skip=skip, limit=limit)
        else:
            slots = parking_slot_crud.get_by_lot(db, lot_id, skip=skip, limit=limit)
    else:
        if available_only:
            slots = parking_slot_crud.get_available(db, skip=skip, limit=limit)
        else:
            slots = parking_slot_crud.get_multi(db, skip=skip, limit=limit)
    
    total = len(slots)
    return ParkingSlotList(slots=slots, total=total)


@router.get("/handicap", response_model=ParkingSlotList)
def get_handicap_slots(lot_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    slots = parking_slot_crud.get_handicap_accessible(db, lot_id)
    return ParkingSlotList(slots=slots, total=len(slots))


@router.get("/by-row/{row_identifier}", response_model=ParkingSlotList)
def get_slots_by_row(row_identifier: str, lot_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    slots = parking_slot_crud.get_by_row(db, row_identifier, lot_id)
    return ParkingSlotList(slots=slots, total=len(slots))


@router.get("/{slot_id}", response_model=ParkingSlotResponse)
def get_parking_slot(slot_id: int, db: Session = Depends(get_db)):
    slot = parking_slot_crud.get(db, slot_id)
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking slot not found"
        )
    return slot


@router.put("/{slot_id}", response_model=ParkingSlotResponse)
def update_parking_slot(slot_id: int, slot_update: ParkingSlotUpdate, db: Session = Depends(get_db)):
    slot = parking_slot_crud.get(db, slot_id)
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking slot not found"
        )
    
    return parking_slot_crud.update(db, db_obj=slot, obj_in=slot_update)


@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_parking_slot(slot_id: int, db: Session = Depends(get_db)):
    slot = parking_slot_crud.get(db, slot_id)
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking slot not found"
        )
    
    parking_slot_crud.remove(db, id=slot_id)