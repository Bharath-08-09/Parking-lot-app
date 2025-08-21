from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.schemas.user_roles import UserRoleCreate, UserRoleUpdate, UserRoleResponse, UserRoleList, UserType, RoleName
from app.crud.user_roles import user_role_crud


router = APIRouter(prefix="/user-roles", tags=["user-roles"])


@router.post("/", response_model=UserRoleResponse, status_code=status.HTTP_201_CREATED)
def create_user_role(user_role: UserRoleCreate, db: Session = Depends(get_db)):
    existing_role = user_role_crud.get_by_user_id(db, user_role.user_id)
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a role assigned"
        )
    
    return user_role_crud.create(db, user_role)


@router.get("/", response_model=UserRoleList)
def get_user_roles(
    skip: int = 0,
    limit: int = 100,
    user_type: Optional[UserType] = Query(None),
    role_name: Optional[RoleName] = Query(None),
    db: Session = Depends(get_db)
):
    user_roles = user_role_crud.get_filtered(
        db, 
        skip=skip, 
        limit=limit,
        user_type=user_type,
        role_name=role_name
    )
    total = len(user_roles)
    return UserRoleList(user_roles=user_roles, total=total)


@router.get("/user/{user_id}", response_model=UserRoleResponse)
def get_user_role_by_user_id(user_id: int, db: Session = Depends(get_db)):
    user_role = user_role_crud.get_by_user_id(db, user_id)
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not found"
        )
    return user_role


@router.get("/{role_id}", response_model=UserRoleResponse)
def get_user_role(role_id: int, db: Session = Depends(get_db)):
    user_role = user_role_crud.get(db, role_id)
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not found"
        )
    return user_role


@router.put("/{role_id}", response_model=UserRoleResponse)
def update_user_role(role_id: int, role_update: UserRoleUpdate, db: Session = Depends(get_db)):
    user_role = user_role_crud.get(db, role_id)
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not found"
        )
    
    return user_role_crud.update(db, db_obj=user_role, obj_in=role_update)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_role(role_id: int, db: Session = Depends(get_db)):
    user_role = user_role_crud.get(db, role_id)
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User role not found"
        )
    
    user_role_crud.remove(db, id=role_id)