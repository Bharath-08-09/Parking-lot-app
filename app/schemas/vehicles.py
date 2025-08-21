from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum


class VehicleType(str, Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    SUV = "SUV"


class VehicleBase(BaseModel):
    plate_number: str
    make: str
    model: Optional[str] = None
    color: str
    vehicle_type: VehicleType
    owner_id: int


class VehicleCreate(VehicleBase):
    @field_validator('plate_number')  
    @classmethod
    def plate_number_must_be_valid(cls, v):
        if not v or not v.strip():
            raise ValueError('Plate number cannot be empty')
        return v.strip().upper()
    
    @field_validator('make')  
    @classmethod
    def make_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Make cannot be empty')
        return v.strip()
    
    @field_validator('color')  
    @classmethod
    def color_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Color cannot be empty')
        return v.strip()


class VehicleUpdate(BaseModel):
    plate_number: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    vehicle_type: Optional[VehicleType] = None
    owner_id: Optional[int] = None


class VehicleResponse(VehicleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)  


class VehicleSearch(BaseModel):
    plate_number: Optional[str] = None
    make: Optional[str] = None
    color: Optional[str] = None
    vehicle_type: Optional[VehicleType] = None
    

class VehicleList(BaseModel):
    vehicles: list[VehicleResponse]
    total: int