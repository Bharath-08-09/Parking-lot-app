from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_roles import UserRoleCreate, UserRoleResponse
from app.crud.user_roles import create_user_role, get_user_role, delete_user_role

router = APIRouter(prefix="/user-roles", tags=["user-roles"])

@router.post("/", response_model=UserRoleResponse, status_code=status.HTTP_201_CREATED)
def create_new_user_role(user_role: UserRoleCreate, db: Session = Depends(get_db)):
    """Create a new user role."""
    # Remove the duplicate check since your CRUD doesn't have get_by_user_id
    return create_user_role(db, user_role)

@router.get("/{role_id}", response_model=UserRoleResponse)
def get_user_role_by_id(role_id: int, db: Session = Depends(get_db)):
    """Get user role by ID."""
    return get_user_role(db, role_id)

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_role_by_id(role_id: int, db: Session = Depends(get_db)):
    """Delete user role by ID."""
    delete_user_role(db, role_id)