from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.drivers import DriverCreate, DriverResponse, DriverList
from app.crud.drivers import create_driver, get_driver, get_handicap_drivers, delete_driver

router = APIRouter(prefix="/drivers", tags=["drivers"])

@router.post("/", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
def create_new_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    """Create a new driver."""
    return create_driver(db, driver)

@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver_by_id(driver_id: int, db: Session = Depends(get_db)):
    """Get driver by ID."""
    return get_driver(db, driver_id)

@router.get("/handicap/", response_model=DriverList)
def get_handicap_drivers_list(db: Session = Depends(get_db)):
    """Get all handicap drivers."""
    drivers = get_handicap_drivers(db)
    return DriverList(drivers=drivers, total=len(drivers))

@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_driver_by_id(driver_id: int, db: Session = Depends(get_db)):
    """Delete a driver."""
    delete_driver(db, driver_id)