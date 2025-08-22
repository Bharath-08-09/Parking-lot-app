from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.lot_notifications import LotNotification
from schemas.lot_notifications import LotNotificationCreate, LotNotificationUpdate

def create_lot_notification(db: Session, payload: LotNotificationCreate) -> LotNotification:
    obj_data = payload.model_dump()
    
    notification = LotNotification(**obj_data)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def get_lot_notification(db: Session, notification_id: int) -> LotNotification:
    notification = db.query(LotNotification).filter(LotNotification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

def update_lot_notification(db: Session, notification_id: int, payload: LotNotificationUpdate) -> LotNotification:
    notification = db.query(LotNotification).filter(LotNotification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(notification, field, value)
    
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def delete_lot_notification(db: Session, notification_id: int) -> LotNotification:
    notification = db.query(LotNotification).filter(LotNotification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    db.delete(notification)
    db.commit()
    return notification