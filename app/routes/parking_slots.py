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
from app.utils.standardised_response import standard_response


router = APIRouter(prefix="/parking-slots", tags=["parking-slots"])


@router.post("/")
def create_new_parking_slot(slot: ParkingSlotCreate, db: Session = Depends(get_db)):
    slot_data = create_parking_slot(db, slot)
    data = ParkingSlotResponse.model_validate(slot_data).model_dump()
    return standard_response(201, "Parking slot created successfully", data)


@router.get("/{slot_id}")
def get_parking_slot_by_id(slot_id: int, db: Session = Depends(get_db)):
    slot_data = get_parking_slot(db, slot_id)
    data = ParkingSlotResponse.model_validate(slot_data).model_dump()
    return standard_response(200, "Parking slot fetched successfully", data)


@router.get("/available/")
def get_available_parking_slots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    slots = get_available_slots(db, skip=skip, limit=limit)
    slot_list = ParkingSlotList(slots=slots, total=len(slots))
    data = slot_list.model_dump()
    return standard_response(200, "Available parking slots fetched successfully", data)


@router.get("/handicap/")
def get_handicap_slots(lot_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    slots = get_handicap_accessible_slots(db, lot_id)
    slot_list = ParkingSlotList(slots=slots, total=len(slots))
    data = slot_list.model_dump()
    return standard_response(200, "Handicap accessible slots fetched successfully", data)


@router.get("/large/")
def get_large_parking_slots(lot_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    slots = get_large_slots(db, lot_id)
    slot_list = ParkingSlotList(slots=slots, total=len(slots))
    data = slot_list.model_dump()
    return standard_response(200, "Large parking slots fetched successfully", data)


@router.put("/{slot_id}")
def update_parking_slot_by_id(slot_id: int, slot_update: ParkingSlotUpdate, db: Session = Depends(get_db)):
    slot_data = update_parking_slot(db, slot_id, slot_update)
    data = ParkingSlotResponse.model_validate(slot_data).model_dump()
    return standard_response(200, "Parking slot updated successfully", data)