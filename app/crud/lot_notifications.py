from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.lot_notifications import LotNotification
from app.schemas.lot_notifications import LotNotificationCreate, LotNotificationUpdate, NotificationType, RecipientType


class LotNotificationCRUD:
    def create(self, db: Session, obj_in: LotNotificationCreate) -> LotNotification:
        db_obj = LotNotification(
            lot_id=obj_in.lot_id,
            notification_type=obj_in.notification_type,
            message=obj_in.message,
            is_sent=obj_in.is_sent,
            recipient_type=obj_in.recipient_type
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[LotNotification]:
        return db.query(LotNotification).filter(LotNotification.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[LotNotification]:
        return db.query(LotNotification).offset(skip).limit(limit).all()

    def get_by_lot(self, db: Session, lot_id: int) -> List[LotNotification]:
        return db.query(LotNotification).filter(LotNotification.lot_id == lot_id).all()

    def get_unsent(self, db: Session) -> List[LotNotification]:
        return db.query(LotNotification).filter(LotNotification.is_sent == False).all()

    def get_by_type(self, db: Session, notification_type: NotificationType) -> List[LotNotification]:
        return db.query(LotNotification).filter(LotNotification.notification_type == notification_type).all()

    def get_by_recipient(self, db: Session, recipient_type: RecipientType) -> List[LotNotification]:
        return db.query(LotNotification).filter(LotNotification.recipient_type == recipient_type).all()

    def get_filtered(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        lot_id: Optional[int] = None,
        notification_type: Optional[NotificationType] = None,
        recipient_type: Optional[RecipientType] = None,
        unsent_only: bool = False
    ) -> List[LotNotification]:
        query = db.query(LotNotification)
        
        if lot_id:
            query = query.filter(LotNotification.lot_id == lot_id)
        
        if notification_type:
            query = query.filter(LotNotification.notification_type == notification_type)
        
        if recipient_type:
            query = query.filter(LotNotification.recipient_type == recipient_type)
        
        if unsent_only:
            query = query.filter(LotNotification.is_sent == False)
        
        return query.offset(skip).limit(limit).all()

    def mark_as_sent(self, db: Session, notification_id: int) -> Optional[LotNotification]:
        notification = self.get(db, notification_id)
        if notification:
            notification.is_sent = True
            db.add(notification)
            db.commit()
            db.refresh(notification)
        return notification

    def mark_multiple_as_sent(self, db: Session, notification_ids: List[int]) -> List[LotNotification]:
        notifications = db.query(LotNotification).filter(
            LotNotification.id.in_(notification_ids)
        ).all()
        
        for notification in notifications:
            notification.is_sent = True
            db.add(notification)
        
        db.commit()
        for notification in notifications:
            db.refresh(notification)
        
        return notifications

    def update(self, db: Session, *, db_obj: LotNotification, obj_in: LotNotificationUpdate) -> LotNotification:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> LotNotification:
        obj = db.query(LotNotification).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def count(self, db: Session, unsent_only: bool = False) -> int:
        if unsent_only:
            return db.query(LotNotification).filter(LotNotification.is_sent == False).count()
        return db.query(LotNotification).count()


lot_notification_crud = LotNotificationCRUD()