from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user_roles import UserRole
from app.schemas.user_roles import UserRoleCreate, UserRoleUpdate, UserType, RoleName
import json


class UserRoleCRUD:
    def create(self, db: Session, obj_in: UserRoleCreate) -> UserRole:
        permissions_json = None
        if obj_in.permissions:
            permissions_json = json.dumps(obj_in.permissions)
        
        db_obj = UserRole(
            user_id=obj_in.user_id,
            user_type=obj_in.user_type,
            role_name=obj_in.role_name,
            permissions=permissions_json
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[UserRole]:
        return db.query(UserRole).filter(UserRole.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[UserRole]:
        return db.query(UserRole).offset(skip).limit(limit).all()

    def get_by_user_id(self, db: Session, user_id: int) -> Optional[UserRole]:
        return db.query(UserRole).filter(UserRole.user_id == user_id).first()

    def get_by_user_type(self, db: Session, user_type: UserType) -> List[UserRole]:
        return db.query(UserRole).filter(UserRole.user_type == user_type).all()

    def get_by_role_name(self, db: Session, role_name: RoleName) -> List[UserRole]:
        return db.query(UserRole).filter(UserRole.role_name == role_name).all()

    def get_filtered(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        user_type: Optional[UserType] = None,
        role_name: Optional[RoleName] = None
    ) -> List[UserRole]:
        query = db.query(UserRole)
        
        if user_type:
            query = query.filter(UserRole.user_type == user_type)
        
        if role_name:
            query = query.filter(UserRole.role_name == role_name)
        
        return query.offset(skip).limit(limit).all()

    def get_admins(self, db: Session) -> List[UserRole]:
        return db.query(UserRole).filter(UserRole.role_name == RoleName.ADMIN).all()

    def get_police_users(self, db: Session) -> List[UserRole]:
        return db.query(UserRole).filter(
            UserRole.user_type.in_([UserType.POLICE, UserType.SECURITY])
        ).all()

    def has_permission(self, db: Session, user_id: int, permission: str) -> bool:
        user_role = self.get_by_user_id(db, user_id)
        if not user_role or not user_role.permissions:
            return False
        
        try:
            permissions = json.loads(user_role.permissions)
            return permission in permissions
        except json.JSONDecodeError:
            return False

    def add_permission(self, db: Session, user_id: int, permission: str) -> Optional[UserRole]:
        user_role = self.get_by_user_id(db, user_id)
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

    def remove_permission(self, db: Session, user_id: int, permission: str) -> Optional[UserRole]:
        user_role = self.get_by_user_id(db, user_id)
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

    def update(self, db: Session, *, db_obj: UserRole, obj_in: UserRoleUpdate) -> UserRole:
        update_data = obj_in.dict(exclude_unset=True)
        
        if "permissions" in update_data and update_data["permissions"] is not None:
            update_data["permissions"] = json.dumps(update_data["permissions"])
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> UserRole:
        obj = db.query(UserRole).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def count(self, db: Session) -> int:
        return db.query(UserRole).count()


user_role_crud = UserRoleCRUD()