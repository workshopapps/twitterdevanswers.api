from fastapi import APIRouter, Request, Depends, status, Path, HTTPException
from fastapi.encoders import jsonable_encoder
from sse_starlette.sse import EventSourceResponse
import asyncio
import logging
from sqlalchemy.orm import Session
from ..database import get_db
from .. import model
from .. import schema
from typing import List

router = APIRouter(
    prefix="/notification",
    tags=["Notification"]
)

MESSAGE_STREAM_DELAY = 2  # second
MESSAGE_STREAM_RETRY_TIMEOUT = 15000  # milisecond

logger = logging.getLogger()


def create_notification(notification: schema.NotificationCreate, db: Session = Depends(get_db)):
    """
    This is background function that should be run after a post request has been made to answer a user's question.
    A NotificationCreate schema should be passed with filled data.
    """

    db_notification = model.Notification(
        owner_id=notification.owner_id,
        content_id=notification.content_id,
        type=notification.type,
        title=notification.title
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def get_user_id():
    # Some jwt verification code should occur here and it should return the user_id or raise an HTTP Unauthorized Exception
    return 1


async def get_notifications(id: int, db: Session):
    """
    This function is responsible for querying the database for the users notifications
    """
    db.commit()
    notifications = db.query(model.Notification).all()
    number_of_unread = len(
        [notification for notification in notifications if notification.unread == True])
    return notifications, number_of_unread


def set_unread_to_false(id: int, db: Session):
    """
    This function sets the unread attribute of the specified notification item to False
    """

    stored_notification = db.query(model.Notification).filter(
        model.Notification.notification_id == id).first()
    if stored_notification is None:
        return False
    stored_notification.unread = False
    #setattr(stored_notification, "unread", False)
    db.commit()
    db.refresh(stored_notification)
    return True


@router.get("/")
async def notification_stream(request: Request, user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    """
    Periodically streams the user's notifications to the client using SSE.
    """

    async def event_generator():
        while True:
            if await request.is_disconnected():
                logger.debug("Request disconnected")
                break

            # Gets the user's notifications
            notifications, number_of_unread = await get_notifications(id=user_id, db=db)
            data = {"number_of_unread": number_of_unread,
                    "notifications": notifications}

            # Streams the data to the client
            yield {
                "event": "new_message",
                "data": jsonable_encoder(data),
                "id": "message_id",
                "retry": MESSAGE_STREAM_RETRY_TIMEOUT
            }

            await asyncio.sleep(MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())


@router.patch("/read/{notification_id}", status_code=status.HTTP_200_OK)
async def mark_read(
    notification_id: int = Path(
        default=..., description="The id of the notification to mark as read"),
    db: Session = Depends(get_db)
):
    """Sets the unread attribute of the specified notification to False."""
    result = set_unread_to_false(id=notification_id, db=db)
    if result is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Notification Id is invalid.")
    return {"success": True}


@router.post("/add/", status_code=status.HTTP_201_CREATED, response_model=schema.Notification)
async def add_notification(notification: schema.NotificationCreate, db: Session = Depends(get_db)):
    db_notification = model.Notification(
        owner_id=notification.owner_id,
        content_id=notification.content_id,
        type=notification.type,
        title=notification.title
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification
