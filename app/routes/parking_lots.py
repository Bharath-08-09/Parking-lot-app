from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.parking_lots import ParkingLotCreate, ParkingLotResponse
from app.crud.parking_lots import create_parking_lot, delete_parking_lot
from app.utils.standardised_response import standard_response

router = APIRouter(prefix="/parking-lots", tags=["parking-lots"])

@router.post("/{lot_id}")
def create_new_parking_lot(lot: ParkingLotCreate, db: Session = Depends(get_db)):
    lot_data = create_parking_lot(db, lot)
    data = ParkingLotResponse.model_validate(lot_data).model_dump()
    return standard_response(201, "Parking lot created successfully", data)

@router.delete("/{lot_id}")
def delete_parking_lot_by_id(lot_id: int, db: Session = Depends(get_db)):
    delete_parking_lot(db, lot_id)
    return standard_response(200, "Parking lot deleted successfully", None)