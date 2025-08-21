from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class ParkingLotBase(BaseModel):
    name: str
    address: Optional[str] = None
    total_capacity: int
    available_slots: int
    is_full: bool = False
    owner_name: str = "Sanjay"

class ParkingLotCreate(ParkingLotBase):
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Lot name cannot be empty')
        return v.strip()
    
    @validator('total_capacity')
    def capacity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Total capacity must be greater than 0')
        return v
    
    @validator('available_slots')
    def available_slots_validation(cls, v, values):
        if 'total_capacity' in values and v > values['total_capacity']:
            raise ValueError('Available slots cannot exceed total capacity')
        if v < 0:
            raise ValueError('Available slots cannot be negative')
        return v

class ParkingLotUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    total_capacity: Optional[int] = None
    available_slots: Optional[int] = None
    is_full: Optional[bool] = None
    owner_name: Optional[str] = None

class ParkingLotResponse(ParkingLotBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ParkingLotStatus(BaseModel):
    id: int
    name: str
    available_slots: int
    total_capacity: int
    is_full: bool
    occupancy_percentage: float

class ParkingLotList(BaseModel):
    lots: list[ParkingLotResponse]
    total: int