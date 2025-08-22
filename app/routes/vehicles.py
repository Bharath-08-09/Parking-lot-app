from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.vehicles import VehicleCreate, VehicleUpdate, VehicleResponse, VehicleList, VehicleSearch, VehicleType
from app.crud.vehicles import create_vehicle, get_vehicle, update_vehicle, delete_vehicle
from app.crud.drivers import get_driver
from app.utils.vehicle_search import ( 
    get_vehicle_by_plate, 
    search_vehicles, 
    get_vehicles_by_owner,
    get_vehicles_by_color,
    get_vehicles_by_make,
    get_vehicles_by_type,
    get_large_vehicles
)

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_new_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    if get_vehicle_by_plate(db, vehicle.plate_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle with this plate number already exists"
        )
    
    try:
        get_driver(db, vehicle.owner_id)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner (driver) not found"
        )
    
    return create_vehicle(db, vehicle)

@router.get("/search", response_model=VehicleList)
def search_vehicles_endpoint(
    plate_number: Optional[str] = Query(None),
    make: Optional[str] = Query(None),
    color: Optional[str] = Query(None),
    vehicle_type: Optional[VehicleType] = Query(None),
    db: Session = Depends(get_db)
):
    search_params = VehicleSearch(
        plate_number=plate_number,
        make=make,
        color=color,
        vehicle_type=vehicle_type
    )
    vehicles = search_vehicles(db, search_params)
    
    return VehicleList(vehicles=vehicles, total=len(vehicles))

@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle_by_id(vehicle_id: int, db: Session = Depends(get_db)):
    return get_vehicle(db, vehicle_id)

@router.get("/plate/{plate_number}", response_model=VehicleResponse)
def get_vehicle_by_plate_number(plate_number: str, db: Session = Depends(get_db)):
    vehicle = get_vehicle_by_plate(db, plate_number)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    return vehicle

@router.get("/owner/{owner_id}", response_model=VehicleList)
def get_vehicles_by_owner_id(owner_id: int, db: Session = Depends(get_db)):
    vehicles = get_vehicles_by_owner(db, owner_id)
    return VehicleList(vehicles=vehicles, total=len(vehicles))

@router.get("/color/{color}", response_model=VehicleList)
def get_vehicles_by_color_filter(color: str, db: Session = Depends(get_db)):
    vehicles = get_vehicles_by_color(db, color)
    return VehicleList(vehicles=vehicles, total=len(vehicles))

@router.get("/make/{make}", response_model=VehicleList)
def get_vehicles_by_make_filter(make: str, db: Session = Depends(get_db)):
    vehicles = get_vehicles_by_make(db, make)
    return VehicleList(vehicles=vehicles, total=len(vehicles))

@router.get("/type/{vehicle_type}", response_model=VehicleList)
def get_vehicles_by_type_filter(vehicle_type: str, db: Session = Depends(get_db)):
    vehicles = get_vehicles_by_type(db, vehicle_type)
    return VehicleList(vehicles=vehicles, total=len(vehicles))

@router.get("/large-vehicles/", response_model=VehicleList)
def get_large_vehicles_endpoint(db: Session = Depends(get_db)):
    vehicles = get_large_vehicles(db)
    return VehicleList(vehicles=vehicles, total=len(vehicles))

@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle_by_id(vehicle_id: int, vehicle_update: VehicleUpdate, db: Session = Depends(get_db)):
    return update_vehicle(db, vehicle_id, vehicle_update)

@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle_by_id(vehicle_id: int, db: Session = Depends(get_db)):
    delete_vehicle(db, vehicle_id)