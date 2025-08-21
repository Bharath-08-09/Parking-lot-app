from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(20), unique=True, nullable=False)
    make = Column(String(50), nullable=False)
    model = Column(String(50))
    color = Column(String(30), nullable=False)
    vehicle_type = Column(String(20), nullable=False)  # Small, Medium, Large, SUV
    owner_id = Column(Integer, ForeignKey("drivers.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner = relationship("Driver", back_populates="vehicles")