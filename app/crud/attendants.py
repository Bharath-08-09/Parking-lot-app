from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.attendants import Attendant
from app.schemas.attendants import AttendantCreate

def create_attendant(db: Session, payload: AttendantCreate) -> Attendant:
    existing = db.query(Attendant).filter(Attendant.employee_id == payload.employee_id.upper()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID already registered")

    obj_data = payload.model_dump()
    if obj_data.get("employee_id"):
        obj_data["employee_id"] = obj_data["employee_id"].upper()
    
    attendant = Attendant(**obj_data)
    db.add(attendant)
    db.commit()
    db.refresh(attendant)
    return attendant

def get_attendant(db: Session, attendant_id: int) -> Attendant:
    attendant = db.query(Attendant).filter(Attendant.id == attendant_id).first()
    if not attendant:
        raise HTTPException(status_code=404, detail="Attendant not found")
    return attendant

def delete_attendant(db: Session, attendant_id: int) -> Attendant:
    attendant = db.query(Attendant).filter(Attendant.id == attendant_id).first()
    if not attendant:
        raise HTTPException(status_code=404, detail="Attendant not found")
    
    db.delete(attendant)
    db.commit()
    return attendant