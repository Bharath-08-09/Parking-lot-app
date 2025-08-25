from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user_roles import UserRole
from app.schemas.user_roles import UserRoleCreate, UserRoleUpdate
import json

def create_user_role(db: Session, payload: UserRoleCreate) -> UserRole:
    """Create a new user role."""
    obj_data = payload.model_dump()
    
    # Convert permissions list to JSON string for storage
    if obj_data.get("permissions"):
        obj_data["permissions"] = json.dumps(obj_data["permissions"])
    
    user_role = UserRole(**obj_data)
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return user_role

def get_user_role(db: Session, role_id: int) -> UserRole:
    """Get user role by ID."""
    user_role = db.query(UserRole).filter(UserRole.id == role_id).first()
    if not user_role:
        raise HTTPException(status_code=404, detail="User role not found")
    return user_role

def delete_user_role(db: Session, role_id: int) -> UserRole:
    """Delete user role by ID."""
    user_role = db.query(UserRole).filter(UserRole.id == role_id).first()
    if not user_role:
        raise HTTPException(status_code=404, detail="User role not found")
    
    db.delete(user_role)
    db.commit()
    return user_role