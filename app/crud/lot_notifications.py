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

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/", response_model=LotNotificationResponse, status_code=status.HTTP_201_CREATED)
def create_notification(notification: LotNotificationCreate, db: Session = Depends(get_db)):
    return create_lot_notification(db, notification)

@router.get("/{notification_id}", response_model=LotNotificationResponse)
def get_notification_by_id(notification_id: int, db: Session = Depends(get_db)):
    return get_lot_notification(db, notification_id)

@router.put("/{notification_id}", response_model=LotNotificationResponse)
def update_notification(notification_id: int, notification_update: LotNotificationUpdate, db: Session = Depends(get_db)):
    return update_lot_notification(db, notification_id, notification_update)

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    delete_lot_notification(db, notification_id)