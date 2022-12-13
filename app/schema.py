from pydantic import BaseModel, EmailStr, validator
from pydantic.types import conint
from datetime import datetime
from typing import Optional, List, Union
from uuid import uuid4, UUID


class AdminPayments(BaseModel):
    question_id: int
    amount: int
    commission: int

    class Config:
        schema_extra = {
            "example": {
                "amount": "50",
                "question_id": "20",
                "commission": "10",
            }
        }


class TransactionRequest(BaseModel):
    amount: int
    user_id: str

    class Config:
        schema_extra = {
            "example": {
                "amount": "50",
                "user_id": "20"
            }
        }


class User(BaseModel):
    user_id:  int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    date_of_birth: str
    gender: str
    description: str
    image_url: str
    phone_number: str
    work_experience: str
    position: str
    stack: str
    links: List[str]
    role: str
    following: str
    followers: str
    location: str
    account_balance: int
    # tokens_earned: int
    # total_likes: int
    created_at : str
    updated_at :str
    is_admin: Optional[bool]

    class Config:
        arbitrary_types_allowed = True


class UserOut(BaseModel):
    user_id:  int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    description: Optional[str]
    image_url: str
    location: str
    account_balance: int


class UserSignInRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirmPassword: str
    email_verification_code: Optional[str]

    @validator('confirmPassword')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class UserSignInAdminRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirmPassword: str
    email_verification_code: Optional[str]
    is_admin: Optional[bool]

    @validator('confirmPassword')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    work_experience: Optional[str] = None
    position: Optional[str] = None
    stack: Optional[str] = None
    links: List[str] = None
    role: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[str] = None


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

    @validator('confirmPassword')
    def passwords_match(cls, v, values, **kwargs):
        if 'newPassword' in values and v != values['newPassword']:
            raise ValueError('passwords do not match')
        return v


class Question(BaseModel):
    title: str
    content: str
    expected_result: str
    payment_amount: int
    answered: bool
    tag: Optional[str]
    # created_at: datetime
    # updated_at: datetime


class QuestionUpdate(BaseModel):
    title: str
    content: str
    expected_result: str
    updated_at: datetime


class Answer(BaseModel):

    id: int
    owner_id: int
    question_id: int
    owner: User
    question: Question


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


class Token(BaseModel):
    data: dict
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class two_factor(Email):
    mfa_hash: str


class TagBase(BaseModel):
    tag_name: str


class TagCreate(TagBase):
    tag_name: str


class Tag(TagBase):
    #tag_id: int
    tag_name: str


class AddQuestionTag(BaseModel):
    tag_id: int
    question_id: int


# class AddTag(BaseModel):
#     tag_id: int
#     # question_id: int


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


class UpdateCorrectAnswerBase(BaseModel):
    """ Answer BaseModel for Update Answer endpoint """

    question_id: int


class UpdateCorrectAnswer(UpdateCorrectAnswerBase):
    """ Answer BaseModel for Update Answer endpoint """
    pass


class LikeBase(BaseModel):
    """ Like BaseModel for Add Like endpoint """

    question_id: int
    like_type: str


class Like(LikeBase):
    """ Like BaseModel for Add Like endpoint """
    pass


class Follow(BaseModel):
    """Schema for Follow endpoint"""
    target_user: int


class Blog(BaseModel):
    title: str
    body: str
    blog_user_id: int
    author: str
    image_url: str
    post_category: str
