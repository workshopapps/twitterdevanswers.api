from pydantic import BaseModel, EmailStr, validator
from pydantic.types import conint
from datetime import datetime
from typing import Optional, List , Union

class UserSignInRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirmPassword: str

    @validator('confirmPassword')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class UserSignInResponse(BaseModel):
    pass



class User(BaseModel):
    user_id:int
    username: Union[str,None] = None
    first_name:  Union[str,None] = None
    last_name:  Union[str,None] = None
    email: EmailStr
    description :  Union[str,None] = None
    phone_number :  Union[str,None] = None
    role :  Union[str,None] = None
    position :  Union[str,None] = None
    stacks :  Union[str,None] = None
    links :Union[str,None] = None
    image_url:  Union[str,None] = None
    location :  Union[str,None] = None
    account_balance :  Union[str,None] = None

    class Config:
        orm_mode = True



class UserUpdate(BaseModel):
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    description: Optional[str]
    role: Optional[str]
    position: Optional[str]
    image_url: Optional[str]
    phone_number: Optional[str]
    location: Optional[str]
    stack: Optional[str]
    link: Optional[str]

    class Config:
        orm_mode = True

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

# class Tag(BaseModel):
#
#    tag_id: int
#    tag_name: str
#
#
# class contenTag(BaseModel):
#    question_id: int
#    tag_id: int
#    question: Question
#    tag: Tag


class TagBase(BaseModel):
    tag_name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    tag_id: int

    class Config:
        orm_mode = True


class AddTag(BaseModel):
    tag_id: int
    question_id: int


class AnswerBase(BaseModel):
    """ Answer BaseModel for Add Answer endpoint """

    question_id: int
    content: str


class CreateAnswer(AnswerBase):
    """ Answer BaseModel for Add Answer endpoint """
    pass


class UpdateAnswerBase(BaseModel):
    """ Answer BaseModel for Update Answer endpoint """

    content: str


class UpdateAnswer(UpdateAnswerBase):
    """ Answer BaseModel for Update Answer endpoint """
    pass


class AnswerVoteBase(BaseModel):
    """ Answer Vote BaseModel for Add Answer Vote endpoint """

    answer_id: int
    vote_type: str


class AnswerVote(AnswerVoteBase):
    """ Answer Vote BaseModel for Add Answer Vote endpoint """
    pass


class Follow(BaseModel):
    user_from: int
    target_user: int
