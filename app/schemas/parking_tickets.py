from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"

class ParkingTicketBase(BaseModel):
    ticket_number: str
    vehicle_id: int
    driver_id: int
    lot_id: int
    slot_id: int
    attendant_id: Optional[int] = None
    entry_time: datetime
    exit_time: Optional[datetime] = None
    parking_fee: Optional[Decimal] = None
    payment_status: PaymentStatus = PaymentStatus.PENDING
    is_active: bool = True

class ParkingTicketCreate(BaseModel):
    vehicle_id: int
    driver_id: int
    lot_id: int
    slot_id: int
    attendant_id: Optional[int] = None
    entry_time: Optional[datetime] = None  

class ParkingTicketUpdate(BaseModel):
    exit_time: Optional[datetime] = None
    parking_fee: Optional[Decimal] = None
    payment_status: Optional[PaymentStatus] = None
    is_active: Optional[bool] = None

class ParkingTicketResponse(ParkingTicketBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ParkingTicketExit(BaseModel):
    ticket_number: str
    exit_time: Optional[datetime] = None  # Will default to current time

class ParkingTicketPayment(BaseModel):
    ticket_number: str
    payment_status: PaymentStatus
    parking_fee: Optional[Decimal] = None

class ActiveParkingResponse(BaseModel):
    id: int
    ticket_number: str
    vehicle_plate: str
    driver_name: str
    lot_name: str
    slot_number: str
    entry_time: datetime
    duration_minutes: int

class ParkingTicketList(BaseModel):
    tickets: list[ParkingTicketResponse]
    total: int