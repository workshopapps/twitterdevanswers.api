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

class ChangePasswordRequest(BaseModel):
    oldPassword : str
    newPassword : str
    confirmPassword: newPassword
class ForgotPassword(BaseModel):
    newPassword : str
    confirmPassword: newPassword

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
class Email(BaseModel):
    email: EmailStr

class TokenData(BaseModel):
    id: Optional[str] = None