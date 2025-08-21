from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Optional
from datetime import datetime


class DriverBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_handicap: bool = False


class DriverCreate(DriverBase):
    name: str
    
    @field_validator('name')  # ✅ Updated from @validator
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class DriverUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_handicap: Optional[bool] = None


class DriverResponse(DriverBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)  # ✅ Updated from Config class


class DriverList(BaseModel):
    drivers: list[DriverResponse]
    total: int