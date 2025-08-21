from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, func
from app.core.database import Base

class LotNotification(Base):
    __tablename__ = "lot_notifications"
    id = Column(Integer, primary_key=True, index=True)
    lot_id = Column(Integer, ForeignKey("parking_lots.id"), nullable=False)
    notification_type = Column(String(30), nullable=False)
    message = Column(Text, nullable=False)
    is_sent = Column(Boolean, default=False)
    recipient_type = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())