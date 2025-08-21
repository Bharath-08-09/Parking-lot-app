from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base

class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    user_type = Column(String(20), nullable=False)
    role_name = Column(String(30), nullable=False)
    permissions = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())