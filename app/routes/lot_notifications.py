from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.lot_notifications import (
    LotNotificationCreate, LotNotificationUpdate, LotNotificationResponse
)
from app.crud.lot_notifications import (
    create_lot_notification,
    get_lot_notification,
    update_lot_notification,
    delete_lot_notification
)
from app.utils.standardised_response import standard_response


router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/")
def create_notification(notification: LotNotificationCreate, db: Session = Depends(get_db)):
    notification_data = create_lot_notification(db, notification)
    data = LotNotificationResponse.model_validate(notification_data).model_dump()
    return standard_response(201, "Notification created successfully", data)


@router.get("/{notification_id}")
def get_notification_by_id(notification_id: int, db: Session = Depends(get_db)):
    notification_data = get_lot_notification(db, notification_id)
    data = LotNotificationResponse.model_validate(notification_data).model_dump()
    return standard_response(200, "Notification fetched successfully", data)


@router.put("/{notification_id}")
def update_notification(notification_id: int, notification_update: LotNotificationUpdate, db: Session = Depends(get_db)):
    notification_data = update_lot_notification(db, notification_id, notification_update)
    data = LotNotificationResponse.model_validate(notification_data).model_dump()
    return standard_response(200, "Notification updated successfully", data)


@router.delete("/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    delete_lot_notification(db, notification_id)
    return standard_response(200, "Notification deleted successfully", None)