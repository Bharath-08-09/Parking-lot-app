from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.attendants import AttendantCreate, AttendantResponse
from app.crud.attendants import create_attendant, get_attendant, delete_attendant

router = APIRouter(prefix="/attendants", tags=["attendants"])

@router.post("/", response_model=AttendantResponse, status_code=status.HTTP_201_CREATED)
def create_new_attendant(attendant: AttendantCreate, db: Session = Depends(get_db)):
    """Create a new attendant."""
    return create_attendant(db, attendant)

@router.get("/{attendant_id}", response_model=AttendantResponse)
def get_attendant_by_id(attendant_id: int, db: Session = Depends(get_db)):
    """Get attendant by ID."""
    return get_attendant(db, attendant_id)

@router.delete("/{attendant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendant_by_id(attendant_id: int, db: Session = Depends(get_db)):
    """Delete an attendant."""
    delete_attendant(db, attendant_id)