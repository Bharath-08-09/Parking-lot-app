from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.drivers import Driver
from app.schemas.drivers import DriverCreate, DriverUpdate


class DriverCRUD:
    def create(self, db: Session, obj_in: DriverCreate) -> Driver:
        db_obj = Driver(
            name=obj_in.name,
            phone=obj_in.phone,
            email=obj_in.email,
            is_handicap=obj_in.is_handicap
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[Driver]:
        return db.query(Driver).filter(Driver.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Driver]:
        return db.query(Driver).offset(skip).limit(limit).all()

    def get_by_phone(self, db: Session, phone: str) -> Optional[Driver]:
        return db.query(Driver).filter(Driver.phone == phone).first()

    def get_by_email(self, db: Session, email: str) -> Optional[Driver]:
        return db.query(Driver).filter(Driver.email == email).first()

    def get_handicap_drivers(self, db: Session) -> List[Driver]:
        return db.query(Driver).filter(Driver.is_handicap == True).all()

    def update(self, db: Session, *, db_obj: Driver, obj_in: DriverUpdate) -> Driver:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Driver:
        obj = db.query(Driver).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def count(self, db: Session) -> int:
        return db.query(Driver).count()


driver_crud = DriverCRUD()