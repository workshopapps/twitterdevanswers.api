from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional


class UserSignInRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username :str
    first_name :str
    last_name :str
    description:str
    image_url : str
    location :str
        

class UserSignInResponse(BaseModel):
    pass


class UserBase(UserSignInRequest):
    user_id: int

    class Config:
        orm_mode = True


class ReadUser(UserBase):
    pass


class ChangePasswordRequest(BaseModel):
    oldPassword: str
    newPassword: str
    confirmPassword: str


class ForgotPassword(BaseModel):
    newPassword: str
    confirmPassword: str
    confirmPassword: str


class ForgotPassword(BaseModel):
    pass


class User(BaseModel):
    id:  int
    user_name: str
    first_name: str
    last_name: str
    email: str
    description : str
    image_url: str
    location : str

class Question(BaseModel):
    content: str
    answered: bool
    created_at: datetime
    updated_at: datetime


class Answer(BaseModel):

    id: int
    owner_id: int
    question_id: int
    owner: User
    question: Question


class Like(BaseModel):
    question_id: int
    dir: conint(le=1)


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


class Tag(BaseModel):

    tag_id: int
    tag_name: str


class contenTag(BaseModel):
    question_id: int
    tag_id: int
    question: Question
    tag: Tag
