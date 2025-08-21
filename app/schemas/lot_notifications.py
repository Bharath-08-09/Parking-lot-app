from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    FULL = "FULL"
    AVAILABLE = "AVAILABLE"
    CAPACITY_WARNING = "CAPACITY_WARNING"


class RecipientType(str, Enum):
    SECURITY = "SECURITY"
    OWNER = "OWNER"
    ATTENDANT = "ATTENDANT"


class LotNotificationBase(BaseModel):
    lot_id: int
    notification_type: NotificationType
    message: str
    is_sent: bool = False
    recipient_type: RecipientType


class LotNotificationCreate(LotNotificationBase):
    @field_validator('message')
    @classmethod
    def message_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()


class LotNotificationUpdate(BaseModel):
    is_sent: Optional[bool] = None
    message: Optional[str] = None


class LotNotificationResponse(LotNotificationBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class LotNotificationList(BaseModel):
    notifications: list[LotNotificationResponse]
    total: int