from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, DECIMAL, func
from app.core.database import Base

class ParkingTicket(Base):
    __tablename__ = "parking_tickets"
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(20), nullable=False, unique=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    lot_id = Column(Integer, ForeignKey("parking_lots.id"), nullable=False)
    slot_id = Column(Integer, ForeignKey("parking_slots.id"), nullable=False)
    attendant_id = Column(Integer, ForeignKey("attendants.id"))
    entry_time = Column(DateTime(timezone=True), nullable=False)
    exit_time = Column(DateTime(timezone=True), nullable=True)
    parking_fee = Column(DECIMAL(10, 2))
    payment_status = Column(String(20), default='pending')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())