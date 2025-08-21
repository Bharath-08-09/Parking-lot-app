from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ParkingSlot(Base):
    __tablename__ = "parking_slots"
    id = Column(Integer, primary_key=True, index=True)
    slot_number = Column(String(10), nullable=False)
    lot_id = Column(Integer, ForeignKey("parking_lots.id"), nullable=False)
    row_identifier = Column(String(5), nullable=False)
    is_occupied = Column(Boolean, default=False)
    is_handicap_accessible = Column(Boolean, default=False)
    distance_from_exit = Column(Integer)
    slot_size = Column(String(20), default='standard')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    lot = relationship("ParkingLot", back_populates="slots")