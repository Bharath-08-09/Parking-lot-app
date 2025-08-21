from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum
import json


class UserType(str, Enum):
    DRIVER = "DRIVER"
    ATTENDANT = "ATTENDANT"
    POLICE = "POLICE"
    SECURITY = "SECURITY"
    OWNER = "OWNER"


class RoleName(str, Enum):
    USER = "USER"
    ATTENDANT = "ATTENDANT"
    ADMIN = "ADMIN"
    POLICE_OFFICER = "POLICE_OFFICER"


class UserRoleBase(BaseModel):
    user_id: int
    user_type: UserType
    role_name: RoleName
    permissions: Optional[List[str]] = None


class UserRoleCreate(UserRoleBase):
    @field_validator('permissions')  # ✅ Updated from @validator
    @classmethod
    def validate_permissions(cls, v):
        if v is not None:
            # Convert list to JSON string for storage
            return v
        return []


class UserRoleUpdate(BaseModel):
    user_id: Optional[int] = None
    user_type: Optional[UserType] = None
    role_name: Optional[RoleName] = None
    permissions: Optional[List[str]] = None


class UserRoleResponse(BaseModel):
    id: int
    user_id: int
    user_type: UserType
    role_name: RoleName
    permissions: Optional[List[str]] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)  # ✅ Updated from Config class


class UserRoleList(BaseModel):
    user_roles: list[UserRoleResponse]
    total: int