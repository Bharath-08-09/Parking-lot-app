from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.parking_lots import ParkingLot
from schemas.parking_lots import ParkingLotCreate

def create_parking_lot(db: Session, payload: ParkingLotCreate) -> ParkingLot:
    obj_data = payload.model_dump()
    
    lot = ParkingLot(**obj_data)
    db.add(lot)
    db.commit()
    db.refresh(lot)
    return lot

def delete_parking_lot(db: Session, lot_id: int) -> ParkingLot:
    lot = db.query(ParkingLot).filter(ParkingLot.id == lot_id).first()
    if not lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")
    
    db.delete(lot)
    db.commit()
    return lot