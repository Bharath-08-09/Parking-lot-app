from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.attendants import AttendantCreate, AttendantUpdate, AttendantResponse, AttendantList
from app.crud.attendants import attendant_crud


router = APIRouter(prefix="/attendants", tags=["attendants"])


@router.post("/", response_model=AttendantResponse, status_code=status.HTTP_201_CREATED)
def create_attendant(attendant: AttendantCreate, db: Session = Depends(get_db)):
    if attendant_crud.get_by_employee_id(db, attendant.employee_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID already exists"
        )
    
    if attendant.phone and attendant_crud.get_by_phone(db, attendant.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )
    
    return attendant_crud.create(db, attendant)


@router.get("/", response_model=AttendantList)
def get_attendants(
    skip: int = 0, 
    limit: int = 100, 
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    if active_only:
        attendants = attendant_crud.get_active(db, skip=skip, limit=limit)
    else:
        attendants = attendant_crud.get_multi(db, skip=skip, limit=limit)
    
    total = attendant_crud.count(db, active_only=active_only)
    return AttendantList(attendants=attendants, total=total)


@router.get("/{attendant_id}", response_model=AttendantResponse)
def get_attendant(attendant_id: int, db: Session = Depends(get_db)):
    attendant = attendant_crud.get(db, attendant_id)
    if not attendant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendant not found"
        )
    return attendant


@router.put("/{attendant_id}", response_model=AttendantResponse)
def update_attendant(attendant_id: int, attendant_update: AttendantUpdate, db: Session = Depends(get_db)):
    attendant = attendant_crud.get(db, attendant_id)
    if not attendant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendant not found"
        )
    
    return attendant_crud.update(db, db_obj=attendant, obj_in=attendant_update)


@router.patch("/{attendant_id}/deactivate", response_model=AttendantResponse)
def deactivate_attendant(attendant_id: int, db: Session = Depends(get_db)):
    attendant = attendant_crud.get(db, attendant_id)
    if not attendant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendant not found"
        )
    
    return attendant_crud.deactivate(db, id=attendant_id)


@router.delete("/{attendant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendant(attendant_id: int, db: Session = Depends(get_db)):
    attendant = attendant_crud.get(db, attendant_id)
    if not attendant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendant not found"
        )
    
    attendant_crud.remove(db, id=attendant_id)