from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.db import get_db, get_current_user
from app.database.models import User, Notification
from app.schemas.agriculture import NotificationResponse

notifications_router = APIRouter(prefix="/notifications", tags=["notifications"])

SAMPLE_NOTIFICATIONS = [
    {
        "id": 1,
        "title": "हवामान इशारा (Weather Alert)",
        "message": "पुढील २४ तासांत हलक्या ते मध्यम स्वरूपाच्या पावसाची शक्यता. फवारणी पुढे ढकलावी.",
        "type": "weather",
        "is_read": False,
        "created_at": "2026-10-17T08:00:00",
    },
    {
        "id": 2,
        "title": "बाजारभाव अपडेट (Market Rate)",
        "message": "पुणे बाजार समितीत सोयाबीनचे भाव ४,८०० रु. प्रति क्विंटल झाले आहेत.",
        "type": "market",
        "is_read": False,
        "created_at": "2026-10-17T09:30:00",
    },
]


@notifications_router.get("", response_model=List[NotificationResponse])
@notifications_router.get("/", response_model=List[NotificationResponse])
async def list_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notifs = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    if not notifs:
        return [NotificationResponse(**n) for n in SAMPLE_NOTIFICATIONS]
    return notifs


@notifications_router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notif = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == current_user.id)
        .first()
    )
    if notif:
        notif.is_read = True
        db.commit()
    return {"status": "success", "notification_id": notification_id}
