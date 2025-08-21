from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
from datetime import datetime


class AttendantBase(BaseModel):
    name: str
    phone: Optional[str] = None
    employee_id: str
    is_active: bool = True


class AttendantCreate(AttendantBase):
    @field_validator('name')  
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @field_validator('employee_id')  
    @classmethod
    def employee_id_must_be_valid(cls, v):
        if not v or not v.strip():
            raise ValueError('Employee ID cannot be empty')
        return v.strip().upper()


class AttendantUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    employee_id: Optional[str] = None
    is_active: Optional[bool] = None


class AttendantResponse(AttendantBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)  


class AttendantList(BaseModel):
    attendants: list[AttendantResponse]
    total: int