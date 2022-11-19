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
    pass 
class ForgotPassword(BaseModel):
    pass 

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


class Question(Base):
   
    id : int
    owner_id: int
    content : str
    answered :bool
    created_at: TIMESTAMP
    updated_at: TIMESTAMP

class Answer(Base):
   
    id:int 
    owner_id: int
    question_id:int
    owner = relationship('User')
    question = relationship('question')

class Notification(Base):

    id : int
    owner_id : int
    content_id: int 
    owner = relationship('user')
    content = relationship('answer')

class Tag(Base):
   
    tag_id: int 
    tag_name: str 

class contenTag(Base):
    
    question_id : int 
    tag_id: int 
    question = relationship('question')
    tag = relationship('tag')
