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
from app.utils.standardised_response import standard_response


router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post("/{vehicle_id}")
def create_new_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    if get_vehicle_by_plate(db, vehicle.plate_number):
        return standard_response(400, "Vehicle with this plate number already exists", None)
    
    try:
        get_driver(db, vehicle.owner_id)
    except HTTPException:
        return standard_response(400, "Owner (driver) not found", None)
    
    vehicle_data = create_vehicle(db, vehicle)
    data = VehicleResponse.model_validate(vehicle_data).model_dump()
    return standard_response(201, "Vehicle created successfully", data)


@router.get("/search")
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
    vehicle_list = VehicleList(vehicles=vehicles, total=len(vehicles))
    data = vehicle_list.model_dump()
    return standard_response(200, "Vehicles searched successfully", data)


@router.get("/{vehicle_id}")
def get_vehicle_by_id(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle_data = get_vehicle(db, vehicle_id)
    data = VehicleResponse.model_validate(vehicle_data).model_dump()
    return standard_response(200, "Vehicle fetched successfully", data)


@router.get("/plate/{plate_number}")
def get_vehicle_by_plate_number(plate_number: str, db: Session = Depends(get_db)):
    vehicle = get_vehicle_by_plate(db, plate_number)
    if not vehicle:
        return standard_response(404, "Vehicle not found", None)
    
    data = VehicleResponse.model_validate(vehicle).model_dump()
    return standard_response(200, "Vehicle fetched successfully", data)


@router.get("/owner/{owner_id}")
def get_vehicles_by_owner_id(owner_id: int, db: Session = Depends(get_db)):
    vehicles = get_vehicles_by_owner(db, owner_id)
    vehicle_list = VehicleList(vehicles=vehicles, total=len(vehicles))
    data = vehicle_list.model_dump()
    return standard_response(200, "Vehicles by owner fetched successfully", data)


@router.get("/color/{color}")
def get_vehicles_by_color_filter(color: str, db: Session = Depends(get_db)):
    vehicles = get_vehicles_by_color(db, color)
    vehicle_list = VehicleList(vehicles=vehicles, total=len(vehicles))
    data = vehicle_list.model_dump()
    return standard_response(200, "Vehicles by color fetched successfully", data)


@router.get("/make/{make}")
def get_vehicles_by_make_filter(make: str, db: Session = Depends(get_db)):
    vehicles = get_vehicles_by_make(db, make)
    vehicle_list = VehicleList(vehicles=vehicles, total=len(vehicles))
    data = vehicle_list.model_dump()
    return standard_response(200, "Vehicles by make fetched successfully", data)


@router.get("/type/{vehicle_type}")
def get_vehicles_by_type_filter(vehicle_type: str, db: Session = Depends(get_db)):
    vehicles = get_vehicles_by_type(db, vehicle_type)
    vehicle_list = VehicleList(vehicles=vehicles, total=len(vehicles))
    data = vehicle_list.model_dump()
    return standard_response(200, "Vehicles by type fetched successfully", data)


@router.get("/large-vehicles/")
def get_large_vehicles_endpoint(db: Session = Depends(get_db)):
    vehicles = get_large_vehicles(db)
    vehicle_list = VehicleList(vehicles=vehicles, total=len(vehicles))
    data = vehicle_list.model_dump()
    return standard_response(200, "Large vehicles fetched successfully", data)


@router.put("/{vehicle_id}")
def update_vehicle_by_id(vehicle_id: int, vehicle_update: VehicleUpdate, db: Session = Depends(get_db)):
    vehicle_data = update_vehicle(db, vehicle_id, vehicle_update)
    data = VehicleResponse.model_validate(vehicle_data).model_dump()
    return standard_response(200, "Vehicle updated successfully", data)


@router.delete("/{vehicle_id}")
def delete_vehicle_by_id(vehicle_id: int, db: Session = Depends(get_db)):
    delete_vehicle(db, vehicle_id)
    return standard_response(200, "Vehicle deleted successfully", None)