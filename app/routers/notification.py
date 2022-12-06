from fastapi import APIRouter, Request, Depends, status, Path, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sse_starlette.sse import EventSourceResponse
import asyncio
import logging
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app import model, schema, oauth

from typing import List

router = APIRouter(
    prefix="/notification",
    tags=['Notification']
)


MESSAGE_STREAM_DELAY = 2  # second
MESSAGE_STREAM_RETRY_TIMEOUT = 15000  # milisecond

logger = logging.getLogger()


def create_notification(notification: schema.NotificationCreate, db: Session):
    """
    This is a background function that should be run after a post request has been made to answer a user's question.
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


async def get_notifications(id: int, db: Session):
    """
    This function is responsible for querying the database for the users notifications
    """
    db.commit()
    notifications = db.query(model.Notification).filter(
        model.Notification.owner_id == id).order_by(desc(model.Notification.notification_id)).all()
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
        return None
    stored_notification.unread = False
    db.commit()
    db.refresh(stored_notification)
    return stored_notification


@router.get("/")
async def notification_stream(request: Request, db: Session = Depends(get_db), token: str = Query(default=..., title="Bearer token", description="The JWT authorization token")):
    """
    Periodically streams the user's notifications to the client using SSE.
    The client communicates with this endpoint using an EventSource object.
    E.g  const source = new EventSource("https://127.0.0.1:8000/notification?token=<user's jwt bearer token>");
    """
    async def event_generator(user_id: int):
        PREVIOUS_NO_UNREAD, FIRST_STREAM = 0, True
        while True:
            if await request.is_disconnected():
                logger.debug("Request disconnected")
                break

            # Gets the user's notifications
            notifications, number_of_unread = await get_notifications(id=user_id, db=db)
            data = {
                "number_of_unread": number_of_unread,
                "notifications": notifications
            }
            if FIRST_STREAM is True:
                # Streams the data to the client
                yield {
                    "event": "new_notification",
                    "data": jsonable_encoder(data),
                    "id": "message_id",
                    "retry": MESSAGE_STREAM_RETRY_TIMEOUT
                }
                FIRST_STREAM = False
                PREVIOUS_NO_UNREAD = number_of_unread

            elif number_of_unread != PREVIOUS_NO_UNREAD:
                # Streams the data to the client
                yield {
                    "event": "new_notification",
                    "data": jsonable_encoder(data),
                    "id": "message_id",
                    "retry": MESSAGE_STREAM_RETRY_TIMEOUT
                }
                PREVIOUS_NO_UNREAD = number_of_unread

            await asyncio.sleep(MESSAGE_STREAM_DELAY)

    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token invalid")
        token = oauth.verify_access_token(
            token=token, credentials_exception=credentials_exception)
    except:
        raise credentials_exception
    return EventSourceResponse(event_generator(token.id))


@router.get("/all")
async def get_all_notifications(db: Session = Depends(get_db), user: schema.User = Depends(oauth.get_current_user)):
    "Get request to list all the notification of the current logged in user."
    notifications, number_of_unread = await get_notifications(user.user_id, db)
    data = {
        "number_of_unread": number_of_unread,
        "notifications": notifications
    }
    return jsonable_encoder(data)


@router.patch("/read/{notification_id}", status_code=status.HTTP_200_OK, response_model=schema.Notification)
async def mark_read(
    notification_id: int = Path(
        default=..., description="The id of the notification to mark as read."
    ),
    db: Session = Depends(get_db),
    user: schema.User = Depends(oauth.get_current_user)
):
    """Sets the unread attribute of the specified notification to False."""
    result = set_unread_to_false(id=notification_id, db=db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Notification Id is invalid."
                            )
    return result


@router.post("/add/", status_code=status.HTTP_201_CREATED, response_model=schema.Notification)
async def add_notification(notification: schema.NotificationCreate, db: Session = Depends(get_db), user: schema.User = Depends(oauth.get_current_user)):
    notification.owner_id = user.user_id
    result = create_notification(notification=notification, db=db)
    return result
