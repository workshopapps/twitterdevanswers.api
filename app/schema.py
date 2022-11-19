from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional 

class UserSignInRequest(BaseModel):
    username: str
    firstname: str
    lastname: str
    password: str
    email: EmailStr
    imageURL: str

class UserSignInResponse(BaseModel):
    pass

class UserBase(UserSignInRequest):
    user_id : int
    class Config:
        orm_mode = True

class ReadUser(UserBase):
    pass

class ChangePasswordRequest(BaseModel):
    pass 
class ForgotPassword(BaseModel):
    pass 

class NotificationBase(BaseModel):
    owner_id: int
    content_id: int
    type: str
    title: str

class NotificationCreate(NotificationBase):
    pass 

class Notification(NotificationBase):
    notification_id: int
    unread: bool = True

    class Config:
        orm_mode = True
