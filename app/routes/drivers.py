from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.drivers import DriverCreate, DriverResponse, DriverList
from app.crud.drivers import create_driver, get_driver, get_handicap_drivers, delete_driver
from app.utils.standardised_response import standard_response


router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.post("/")
def create_new_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    """Create a new driver."""
    driver_data = create_driver(db, driver)
    data = DriverResponse.model_validate(driver_data).model_dump()
    return standard_response(201, "Driver created successfully", data)


@router.get("/{driver_id}")
def get_driver_by_id(driver_id: int, db: Session = Depends(get_db)):
    """Get driver by ID."""
    driver_data = get_driver(db, driver_id)
    data = DriverResponse.model_validate(driver_data).model_dump()
    return standard_response(200, "Driver fetched successfully", data)


@router.get("/handicap/")
def get_handicap_drivers_list(db: Session = Depends(get_db)):
    """Get all handicap drivers."""
    drivers = get_handicap_drivers(db)
    driver_list = DriverList(drivers=drivers, total=len(drivers))
    data = driver_list.model_dump()
    return standard_response(200, "Handicap drivers fetched successfully", data)


@router.delete("/{driver_id}")
def delete_driver_by_id(driver_id: int, db: Session = Depends(get_db)):
    """Delete a driver."""
    delete_driver(db, driver_id)
    return standard_response(200, "Driver deleted successfully", None)
