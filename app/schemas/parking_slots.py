from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class SlotSize(str, Enum):
    COMPACT = "compact"
    STANDARD = "standard"
    LARGE = "large"


class ParkingSlotBase(BaseModel):
    slot_number: str
    lot_id: int
    row_identifier: str
    is_occupied: bool = False
    is_handicap_accessible: bool = False
    distance_from_exit: Optional[int] = None
    slot_size: SlotSize = SlotSize.STANDARD


class ParkingSlotCreate(ParkingSlotBase):
    @field_validator('slot_number')  
    @classmethod
    def slot_number_must_be_valid(cls, v):
        if not v or not v.strip():
            raise ValueError('Slot number cannot be empty')
        return v.strip().upper()
    
    @field_validator('row_identifier')  
    @classmethod
    def row_identifier_must_be_valid(cls, v):
        if not v or not v.strip():
            raise ValueError('Row identifier cannot be empty')
        return v.strip().upper()
    
    @field_validator('distance_from_exit')  
    @classmethod
    def distance_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('Distance from exit cannot be negative')
        return v


class ParkingSlotUpdate(BaseModel):
    slot_number: Optional[str] = None
    lot_id: Optional[int] = None
    row_identifier: Optional[str] = None
    is_occupied: Optional[bool] = None
    is_handicap_accessible: Optional[bool] = None
    distance_from_exit: Optional[int] = None
    slot_size: Optional[SlotSize] = None

class ParkingSlotResponse(ParkingSlotBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ParkingSlotAvailability(BaseModel):
    id: int
    slot_number: str
    lot_id: int
    row_identifier: str
    is_occupied: bool
    is_handicap_accessible: bool
    slot_size: SlotSize

class ParkingSlotList(BaseModel):
    slots: list[ParkingSlotResponse]
    total: int