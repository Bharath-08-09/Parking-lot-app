from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.core.database import Base

class Attendant(Base):
    __tablename__ = "attendants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True)
    employee_id = Column(String(20), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())