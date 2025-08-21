from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.attendants import Attendant
from app.schemas.attendants import AttendantCreate, AttendantUpdate


class AttendantCRUD:
    def create(self, db: Session, obj_in: AttendantCreate) -> Attendant:
        db_obj = Attendant(
            name=obj_in.name,
            phone=obj_in.phone,
            employee_id=obj_in.employee_id.upper(),
            is_active=obj_in.is_active
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[Attendant]:
        return db.query(Attendant).filter(Attendant.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Attendant]:
        return db.query(Attendant).offset(skip).limit(limit).all()

    def get_by_employee_id(self, db: Session, employee_id: str) -> Optional[Attendant]:
        return db.query(Attendant).filter(Attendant.employee_id == employee_id.upper()).first()

    def get_by_phone(self, db: Session, phone: str) -> Optional[Attendant]:
        return db.query(Attendant).filter(Attendant.phone == phone).first()

    def get_active(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Attendant]:
        return db.query(Attendant).filter(Attendant.is_active == True).offset(skip).limit(limit).all()

    def get_available_attendants(self, db: Session) -> List[Attendant]:
        return db.query(Attendant).filter(Attendant.is_active == True).all()

    def update(self, db: Session, *, db_obj: Attendant, obj_in: AttendantUpdate) -> Attendant:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "employee_id" and value:
                value = value.upper()
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def deactivate(self, db: Session, *, id: int) -> Attendant:
        attendant = self.get(db, id)
        attendant.is_active = False
        db.add(attendant)
        db.commit()
        db.refresh(attendant)
        return attendant

    def remove(self, db: Session, *, id: int) -> Attendant:
        obj = db.query(Attendant).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def count(self, db: Session, active_only: bool = False) -> int:
        if active_only:
            return db.query(Attendant).filter(Attendant.is_active == True).count()
        return db.query(Attendant).count()


attendant_crud = AttendantCRUD()