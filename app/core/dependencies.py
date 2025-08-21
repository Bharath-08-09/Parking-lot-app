from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from schemas.user_roles import UserType, RoleName

# Keep HTTPBearer only in dependencies.py
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> dict:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    payload = verify_token(token)
    
    user_id = payload.get("sub")
    user_type = payload.get("user_type")
    role_name = payload.get("role_name")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "user_id": int(user_id),
        "user_type": user_type,
        "role_name": role_name
    }

def require_role(required_roles: list[RoleName]):
    """Dependency to require specific roles."""
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role_name")
        # Convert enum values to strings for comparison
        allowed_roles = [role.value for role in required_roles]
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

def require_user_type(required_types: list[UserType]):
    """Dependency to require specific user types."""
    def type_checker(current_user: dict = Depends(get_current_user)):
        user_type = current_user.get("user_type")
        # Convert enum values to strings for comparison
        allowed_types = [utype.value for utype in required_types]
        if user_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied for this user type"
            )
        return current_user
    return type_checker

# Specific role dependencies for common use cases
admin_required = require_role([RoleName.ADMIN])
attendant_required = require_role([RoleName.ATTENDANT, RoleName.ADMIN])
police_required = require_user_type([UserType.POLICE, UserType.SECURITY])