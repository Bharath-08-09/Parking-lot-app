from sqlalchemy.orm import Session
from app.crud.lot_notifications import lot_notification_crud
from app.schemas.lot_notifications import LotNotificationCreate, NotificationType


class NotificationService:
    def notify_lot_full(self, db: Session, lot_id: int, message: str = "Lot is full"):
        notification = LotNotificationCreate(
            lot_id=lot_id,
            notification_type=NotificationType.FULL,
            message=message,
            is_sent=False,
            recipient_type="OWNER"
        )
        return lot_notification_crud.create(db, notification)

    def notify_capacity_warning(self, db: Session, lot_id: int, available: int):
        message = f"Warning: Capacity low. Only {available} slots left."
        notification = LotNotificationCreate(
            lot_id=lot_id,
            notification_type=NotificationType.CAPACITY_WARNING,
            message=message,
            is_sent=False,
            recipient_type="SECURITY"
        )
        return lot_notification_crud.create(db, notification)


notification_service = NotificationService()