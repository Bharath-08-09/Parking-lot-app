from pydantic import BaseModel
from app.schemas.user_roles import UserType, RoleName  # adjust import as needed

class LoginRequest(BaseModel):
    user_id: int
    user_type: UserType

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_type: UserType
    role_name: RoleName