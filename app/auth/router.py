from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.auth_schema import LoginRequest, LoginResponse
from app.schemas.user_roles import UserType, RoleName

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Here you would verify credentials and user existence

    # Example role mapping (move this logic to a service if desired)
    role_mapping = {
        UserType.DRIVER: RoleName.USER,
        UserType.ATTENDANT: RoleName.ATTENDANT,
        UserType.POLICE: RoleName.POLICE_OFFICER,
        UserType.SECURITY: RoleName.ADMIN,
        UserType.OWNER: RoleName.ADMIN
    }
    role_name = role_mapping.get(login_data.user_type, RoleName.USER)

    token_data = {
        "sub": str(login_data.user_id),
        "user_type": login_data.user_type.value,
        "role_name": role_name.value
    }
    access_token = create_access_token(data=token_data)

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_type=login_data.user_type,
        role_name=role_name
    )