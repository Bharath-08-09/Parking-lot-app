from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.parking_slots import ParkingSlotCreate, ParkingSlotUpdate, ParkingSlotResponse, ParkingSlotList
from app.crud.parking_slots import (
    create_parking_slot,
    get_parking_slot,
    get_available_slots,
    get_handicap_accessible_slots,
    get_large_slots,
    update_parking_slot
)

router = APIRouter(prefix="/parking-slots", tags=["parking-slots"])

@router.post("/", response_model=ParkingSlotResponse, status_code=status.HTTP_201_CREATED)
def create_new_parking_slot(slot: ParkingSlotCreate, db: Session = Depends(get_db)):
    """Create a new parking slot."""
    return create_parking_slot(db, slot)

@router.get("/{slot_id}", response_model=ParkingSlotResponse)
def get_parking_slot_by_id(slot_id: int, db: Session = Depends(get_db)):
    """Get parking slot by ID."""
    return get_parking_slot(db, slot_id)

@router.get("/available/", response_model=ParkingSlotList)
def get_available_parking_slots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all available parking slots."""
    slots = get_available_slots(db, skip=skip, limit=limit)
    return ParkingSlotList(slots=slots, total=len(slots))

@router.get("/handicap/", response_model=ParkingSlotList)
def get_handicap_slots(lot_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Get handicap accessible slots."""
    slots = get_handicap_accessible_slots(db, lot_id)
    return ParkingSlotList(slots=slots, total=len(slots))

@router.get("/large/", response_model=ParkingSlotList)
def get_large_parking_slots(lot_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Get large slots for big vehicles."""
    slots = get_large_slots(db, lot_id)
    return ParkingSlotList(slots=slots, total=len(slots))

@router.put("/{slot_id}", response_model=ParkingSlotResponse)
def update_parking_slot_by_id(slot_id: int, slot_update: ParkingSlotUpdate, db: Session = Depends(get_db)):
    """Update parking slot."""
    return update_parking_slot(db, slot_id, slot_update)