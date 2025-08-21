from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ParkingLot(Base):
    __tablename__ = "parking_lots"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(Text)
    total_capacity = Column(Integer, nullable=False)
    available_slots = Column(Integer, nullable=False)
    is_full = Column(Boolean, default=False)
    owner_name = Column(String(100), default='Sanjay')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    slots = relationship("ParkingSlot", back_populates="lot")