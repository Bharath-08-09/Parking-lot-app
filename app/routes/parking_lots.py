from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.parking_lots import ParkingLotCreate, ParkingLotResponse
from app.crud.parking_lots import create_parking_lot, delete_parking_lot

router = APIRouter(prefix="/parking-lots", tags=["parking-lots"])

@router.post("/", response_model=ParkingLotResponse, status_code=status.HTTP_201_CREATED)
def create_new_parking_lot(lot: ParkingLotCreate, db: Session = Depends(get_db)):
    return create_parking_lot(db, lot)

@router.delete("/{lot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_parking_lot_by_id(lot_id: int, db: Session = Depends(get_db)):
    delete_parking_lot(db, lot_id)