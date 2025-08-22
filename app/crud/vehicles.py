from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.vehicles import Vehicle
from app.schemas.vehicles import VehicleCreate, VehicleUpdate

def create_vehicle(db: Session, payload: VehicleCreate) -> Vehicle:
    """Create a new vehicle."""
    obj_data = payload.model_dump()
    
    # Convert plate_number to uppercase
    if obj_data.get("plate_number"):
        obj_data["plate_number"] = obj_data["plate_number"].upper()
    
    vehicle = Vehicle(**obj_data)
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle

def get_vehicle(db: Session, vehicle_id: int) -> Vehicle:
    """Get vehicle by ID."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

def update_vehicle(db: Session, vehicle_id: int, payload: VehicleUpdate) -> Vehicle:
    """Update vehicle information."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "plate_number" and value:
            value = value.upper()
        setattr(vehicle, field, value)
    
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle

def delete_vehicle(db: Session, vehicle_id: int) -> Vehicle:
    """Delete vehicle by ID."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db.delete(vehicle)
    db.commit()
    return vehicle