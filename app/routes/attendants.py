from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.attendants import AttendantCreate, AttendantResponse
from app.crud.attendants import create_attendant, get_attendant, delete_attendant
from app.utils.standardised_response import standard_response


router = APIRouter(prefix="/attendants", tags=["attendants"])


@router.post("/")
def create_new_attendant(attendant: AttendantCreate, db: Session = Depends(get_db)):
    """Create a new attendant."""
    attendant_data = create_attendant(db, attendant)
    data = AttendantResponse.model_validate(attendant_data).model_dump()
    return standard_response(201, "Attendant created successfully", data)


@router.get("/{attendant_id}")
def get_attendant_by_id(attendant_id: int, db: Session = Depends(get_db)):
    """Get attendant by ID."""
    attendant_data = get_attendant(db, attendant_id)
    data = AttendantResponse.model_validate(attendant_data).model_dump()
    return standard_response(200, "Attendant fetched successfully", data)


@router.delete("/{attendant_id}")
def delete_attendant_by_id(attendant_id: int, db: Session = Depends(get_db)):
    """Delete an attendant."""
    delete_attendant(db, attendant_id)
    return standard_response(200, "Attendant deleted successfully", None)