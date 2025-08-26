from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_roles import UserRoleCreate, UserRoleResponse
from app.crud.user_roles import create_user_role, get_user_role, delete_user_role
from app.utils.standardised_response import standard_response


router = APIRouter(prefix="/user-roles", tags=["user-roles"])


@router.post("/{role_id}")
def create_new_user_role(user_role: UserRoleCreate, db: Session = Depends(get_db)):
    # Remove the duplicate check since your CRUD doesn't have get_by_user_id
    user_role_data = create_user_role(db, user_role)
    data = UserRoleResponse.model_validate(user_role_data).model_dump()
    return standard_response(201, "User role created successfully", data)


@router.get("/{role_id}")
def get_user_role_by_id(role_id: int, db: Session = Depends(get_db)):
    user_role_data = get_user_role(db, role_id)
    data = UserRoleResponse.model_validate(user_role_data).model_dump()
    return standard_response(200, "User role fetched successfully", data)


@router.delete("/{role_id}")
def delete_user_role_by_id(role_id: int, db: Session = Depends(get_db)):
    delete_user_role(db, role_id)
    return standard_response(200, "User role deleted successfully", None)