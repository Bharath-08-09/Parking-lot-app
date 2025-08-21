from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.schemas.lot_notifications import (
    LotNotificationCreate, LotNotificationUpdate, LotNotificationResponse, 
    LotNotificationList, NotificationType, RecipientType
)
from app.crud.lot_notifications import lot_notification_crud


router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/", response_model=LotNotificationResponse, status_code=status.HTTP_201_CREATED)
def create_notification(notification: LotNotificationCreate, db: Session = Depends(get_db)):
    return lot_notification_crud.create(db, notification)


@router.get("/", response_model=LotNotificationList)
def get_notifications(
    skip: int = 0,
    limit: int = 100,
    lot_id: Optional[int] = Query(None),
    notification_type: Optional[NotificationType] = Query(None),
    recipient_type: Optional[RecipientType] = Query(None),
    unsent_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    notifications = lot_notification_crud.get_filtered(
        db, 
        skip=skip, 
        limit=limit,
        lot_id=lot_id,
        notification_type=notification_type,
        recipient_type=recipient_type,
        unsent_only=unsent_only
    )
    total = len(notifications)
    return LotNotificationList(notifications=notifications, total=total)


@router.get("/unsent", response_model=LotNotificationList)
def get_unsent_notifications(db: Session = Depends(get_db)):
    notifications = lot_notification_crud.get_unsent(db)
    return LotNotificationList(notifications=notifications, total=len(notifications))


@router.get("/{notification_id}", response_model=LotNotificationResponse)
def get_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = lot_notification_crud.get(db, notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return notification


@router.patch("/{notification_id}/mark-sent", response_model=LotNotificationResponse)
def mark_notification_sent(notification_id: int, db: Session = Depends(get_db)):
    notification = lot_notification_crud.mark_as_sent(db, notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return notification


@router.put("/{notification_id}", response_model=LotNotificationResponse)
def update_notification(notification_id: int, notification_update: LotNotificationUpdate, db: Session = Depends(get_db)):
    notification = lot_notification_crud.get(db, notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    return lot_notification_crud.update(db, db_obj=notification, obj_in=notification_update)


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = lot_notification_crud.get(db, notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    lot_notification_crud.remove(db, id=notification_id)