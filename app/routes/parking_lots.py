from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.parking_lots import ParkingLotCreate, ParkingLotUpdate, ParkingLotResponse, ParkingLotList, ParkingLotStatus
from app.crud.parking_lots import parking_lot_crud


router = APIRouter(prefix="/parking-lots", tags=["parking-lots"])


@router.post("/", response_model=ParkingLotResponse, status_code=status.HTTP_201_CREATED)
def create_parking_lot(lot: ParkingLotCreate, db: Session = Depends(get_db)):
    if parking_lot_crud.get_by_name(db, lot.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parking lot with this name already exists"
        )
    
    return parking_lot_crud.create(db, lot)


@router.get("/", response_model=ParkingLotList)
def get_parking_lots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lots = parking_lot_crud.get_multi(db, skip=skip, limit=limit)
    total = parking_lot_crud.count(db)
    return ParkingLotList(lots=lots, total=total)


@router.get("/status", response_model=list[ParkingLotStatus])
def get_lots_status(db: Session = Depends(get_db)):
    lots = parking_lot_crud.get_multi(db)
    status_list = []
    
    for lot in lots:
        occupancy_percentage = ((lot.total_capacity - lot.available_slots) / lot.total_capacity) * 100
        status_list.append(ParkingLotStatus(
            id=lot.id,
            name=lot.name,
            available_slots=lot.available_slots,
            total_capacity=lot.total_capacity,
            is_full=lot.is_full,
            occupancy_percentage=round(occupancy_percentage, 2)
        ))
    
    return status_list


@router.get("/available", response_model=ParkingLotList)
def get_available_lots(db: Session = Depends(get_db)):
    lots = parking_lot_crud.get_available(db)
    return ParkingLotList(lots=lots, total=len(lots))


@router.get("/{lot_id}", response_model=ParkingLotResponse)
def get_parking_lot(lot_id: int, db: Session = Depends(get_db)):
    lot = parking_lot_crud.get(db, lot_id)
    if not lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking lot not found"
        )
    return lot


@router.put("/{lot_id}", response_model=ParkingLotResponse)
def update_parking_lot(lot_id: int, lot_update: ParkingLotUpdate, db: Session = Depends(get_db)):
    lot = parking_lot_crud.get(db, lot_id)
    if not lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking lot not found"
        )
    
    return parking_lot_crud.update(db, db_obj=lot, obj_in=lot_update)


@router.delete("/{lot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_parking_lot(lot_id: int, db: Session = Depends(get_db)):
    lot = parking_lot_crud.get(db, lot_id)
    if not lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking lot not found"
        )
    
    parking_lot_crud.remove(db, id=lot_id)