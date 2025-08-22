from sqlalchemy.orm import Session
from typing import List, Optional
from models.user_roles import UserRole
from schemas.user_roles import UserType, RoleName
import json

def get_user_role_by_user_id(db: Session, user_id: int) -> Optional[UserRole]:
    """Get user role by user ID."""
    return db.query(UserRole).filter(UserRole.user_id == user_id).first()

def get_admins(db: Session) -> List[UserRole]:
    """Get all admin users."""
    return db.query(UserRole).filter(UserRole.role_name == RoleName.ADMIN).all()

def get_police_users(db: Session) -> List[UserRole]:
    """Get all police users."""
    return db.query(UserRole).filter(
        UserRole.user_type.in_([UserType.POLICE, UserType.SECURITY])
    ).all()

def has_permission(db: Session, user_id: int, permission: str) -> bool:
    """Check if user has a specific permission."""
    user_role = get_user_role_by_user_id(db, user_id)
    if not user_role or not user_role.permissions:
        return False
    
    try:
        permissions = json.loads(user_role.permissions)
        return permission in permissions
    except json.JSONDecodeError:
        return False

def add_permission(db: Session, user_id: int, permission: str) -> Optional[UserRole]:
    """Add a permission to user."""
    user_role = get_user_role_by_user_id(db, user_id)
    if not user_role:
        return None
    
    try:
        permissions = json.loads(user_role.permissions) if user_role.permissions else []
        if permission not in permissions:
            permissions.append(permission)
            user_role.permissions = json.dumps(permissions)
            db.add(user_role)
            db.commit()
            db.refresh(user_role)
    except json.JSONDecodeError:
        user_role.permissions = json.dumps([permission])
        db.add(user_role)
        db.commit()
        db.refresh(user_role)
    
    return user_role

def remove_permission(db: Session, user_id: int, permission: str) -> Optional[UserRole]:
    """Remove a permission from user."""
    user_role = get_user_role_by_user_id(db, user_id)
    if not user_role or not user_role.permissions:
        return user_role
    
    try:
        permissions = json.loads(user_role.permissions)
        if permission in permissions:
            permissions.remove(permission)
            user_role.permissions = json.dumps(permissions)
            db.add(user_role)
            db.commit()
            db.refresh(user_role)
    except json.JSONDecodeError:
        pass
    
    return user_role