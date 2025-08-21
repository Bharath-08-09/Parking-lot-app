from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.drivers import DriverCreate, DriverUpdate, DriverResponse, DriverList
from app.crud.drivers import driver_crud


router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.post("/", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    if driver.phone and driver_crud.get_by_phone(db, driver.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )
    if driver.email and driver_crud.get_by_email(db, driver.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return driver_crud.create(db, driver)


@router.get("/", response_model=DriverList)
def get_drivers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    drivers = driver_crud.get_multi(db, skip=skip, limit=limit)
    total = driver_crud.count(db)
    return DriverList(drivers=drivers, total=total)


@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = driver_crud.get(db, driver_id)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )
    return driver


@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(driver_id: int, driver_update: DriverUpdate, db: Session = Depends(get_db)):
    driver = driver_crud.get(db, driver_id)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )
    
    return driver_crud.update(db, db_obj=driver, obj_in=driver_update)


@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = driver_crud.get(db, driver_id)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )
    
    driver_crud.remove(db, id=driver_id)