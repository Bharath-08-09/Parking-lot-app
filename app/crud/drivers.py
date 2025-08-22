from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from models.drivers import Driver
from schemas.drivers import DriverCreate

def create_driver(db: Session, payload: DriverCreate) -> Driver:
    obj_data = payload.model_dump()
    
    driver = Driver(**obj_data)
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver

def get_driver(db: Session, driver_id: int) -> Driver:
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

def get_handicap_drivers(db: Session) -> List[Driver]:
    """Get all handicap drivers."""
    return db.query(Driver).filter(Driver.is_handicap == True).all()

def delete_driver(db: Session, driver_id: int) -> Driver:
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    db.delete(driver)
    db.commit()
    return driver