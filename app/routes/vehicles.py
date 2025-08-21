from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.vehicles import VehicleCreate, VehicleUpdate, VehicleResponse, VehicleList, VehicleSearch, VehicleType
from app.crud.vehicles import vehicle_crud
from app.crud.drivers import driver_crud

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    """Create a new vehicle."""
    # Check if plate number already exists
    if vehicle_crud.get_by_plate(db, vehicle.plate_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle with this plate number already exists"
        )
    
    # Check if owner exists
    if not driver_crud.get(db, vehicle.owner_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner (driver) not found"
        )
    
    return vehicle_crud.create(db, vehicle)

@router.get("/", response_model=VehicleList)
def get_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all vehicles with pagination."""
    vehicles = vehicle_crud.get_multi(db, skip=skip, limit=limit)
    total = vehicle_crud.count(db)
    return VehicleList(vehicles=vehicles, total=total)

@router.get("/search", response_model=VehicleList)
def search_vehicles(
    plate_number: Optional[str] = Query(None),
    make: Optional[str] = Query(None),
    color: Optional[str] = Query(None),
    vehicle_type: Optional[VehicleType] = Query(None),
    db: Session = Depends(get_db)
):
    """Search vehicles by various criteria (UC12-UC16)."""
    search_params = VehicleSearch(
        plate_number=plate_number,
        make=make,
        color=color,
        vehicle_type=vehicle_type
    )
    vehicles = vehicle_crud.search(db, search_params)
    
    # Convert SQLAlchemy objects to Pydantic models
    vehicle_responses = [
        VehicleResponse(
            id=vehicle.id,
            plate_number=vehicle.plate_number,
            make=vehicle.make,
            model=vehicle.model,
            color=vehicle.color,
            vehicle_type=vehicle.vehicle_type,
            owner_id=vehicle.owner_id,
            created_at=vehicle.created_at,
            updated_at=vehicle.updated_at
        ) for vehicle in vehicles
    ]
    
    return VehicleList(vehicles=vehicle_responses, total=len(vehicle_responses))


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Get vehicle by ID."""
    vehicle = vehicle_crud.get(db, vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    return vehicle

@router.get("/plate/{plate_number}", response_model=VehicleResponse)
def get_vehicle_by_plate(plate_number: str, db: Session = Depends(get_db)):
    """Get vehicle by plate number."""
    vehicle = vehicle_crud.get_by_plate(db, plate_number)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    return vehicle

@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(vehicle_id: int, vehicle_update: VehicleUpdate, db: Session = Depends(get_db)):
    """Update vehicle information."""
    vehicle = vehicle_crud.get(db, vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    return vehicle_crud.update(db, db_obj=vehicle, obj_in=vehicle_update)

@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Delete a vehicle."""
    vehicle = vehicle_crud.get(db, vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    vehicle_crud.remove(db, id=vehicle_id)