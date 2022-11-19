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
    confirmPassword: str
class ForgotPassword(BaseModel):
    pass 

<<<<<<< HEAD
class User(BaseModel):
    id :  int
    user_name: str
    first_name: str
    last_name : str
    email: str
    password_hash : str
    account_balance: int
    role: str
    image_url: str


class Question(BaseModel):
   
    id : int
    owner_id: int
    content : str
    answered :bool
    created_at: TIMESTAMP
    updated_at: TIMESTAMP

class Answer(BaseModel):
   
    id:int 
    owner_id: int
    question_id:int
    owner = relationship('User')
    question = relationship('question')

class Notification(BaseModel):

    id : int
    owner_id : int
    content_id: int 
    owner = relationship('user')
    content = relationship('answer')

class Tag(BaseModel):
   
    tag_id: int 
    tag_name: str 

class contenTag(BaseModel):
    question_id : int 
    tag_id: int 
    question = relationship('question')
    tag = relationship('tag')
=======
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
>>>>>>> b80b82bf9cfa547fedd6e6788536d788f4a8a52f
