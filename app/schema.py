from pydantic import BaseModel, EmailStr, validator
from pydantic.types import conint
from datetime import datetime
from typing import Optional, List, Union
from uuid import uuid4, UUID


class AdminPayments(BaseModel):
    question_id: str
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
    user_id:  str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    date_of_birth: str
    gender: str
    description: str
    image_url: str
    phone_number: str
    organization: str
    work_experience: str
    position: str
    stack: str
    links: List[str]
    role: str
    following: str
    followers: str
    location: str
    account_balance: int
    tokens_earned: int
    total_likes: int
    created_at: str
    is_admin: Optional[bool]

    class Config:
        arbitrary_types_allowed = True


class UserOut(BaseModel):
    user_id:  str
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
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    confirmPassword: str

    @validator('confirmPassword')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class UserSignInAdminRequest(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    confirmPassword: str
    is_admin: Optional[bool]

    @validator('confirmPassword')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class UserVerification(BaseModel):
    email: EmailStr
    verification_code: int


class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    organization: Optional[str] = None
    work_experience: Optional[str] = None
    position: Optional[str] = None
    stack: Optional[str] = None
    links: Optional[str] = None
    role: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[str] = None

    
class UserSignInResponse(BaseModel):
    pass


class UserBase(UserSignInRequest):
    user_id: str

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
    # created_at: datetime = datetime.now()
    # updated_at: datetime = datetime.now()


class QuestionUpdate(BaseModel):
    title: str
    content: str
    expected_result: str
    # updated_at: datetime = datetime.now()


class Answer(BaseModel):

    id: str
    owner_id: str
    question_id: str
    owner: User
    question: Question
    created_at: datetime = datetime.now()


class NotificationBase(BaseModel):
    owner_id: str
    content_id: str
    type: str
    title: str


class NotificationCreate(NotificationBase):
    pass


class Notification(NotificationBase):
    notification_id: str
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
    tag_id: str
    question_id: str


# class AddTag(BaseModel):
#     tag_id: int
#     # question_id: int


class AnswerBase(BaseModel):
    """ Answer BaseModel for Add Answer endpoint """

    question_id: str
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

    answer_id: str
    vote_type: str


class AnswerVote(AnswerVoteBase):
    """ Answer Vote BaseModel for Add Answer Vote endpoint """
    pass


class UpdateCorrectAnswerBase(BaseModel):
    """ Answer BaseModel for Update Answer endpoint """

    question_id: str


class UpdateCorrectAnswer(UpdateCorrectAnswerBase):
    """ Answer BaseModel for Update Answer endpoint """
    pass


class LikeBase(BaseModel):
    """ Like BaseModel for Add Like endpoint """

    question_id: str
    like_type: str


class Like(LikeBase):
    """ Like BaseModel for Add Like endpoint """
    pass


class Follow(BaseModel):
    """Schema for Follow endpoint"""
    target_user: str


class Blog(BaseModel):
    title: str
    body: str
    blog_user_id: str
    author: str
    image_url: str
    post_category: str


class Community(BaseModel):
    community_id: str
    user_id: str
    name: str
    description: str
    image_url: str
    total_members: int
    created_at: str
    updated_at: str 


class AddCommunity(BaseModel):
    name :str
    description :str
    image_url : str


class UpdateCommunity(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class Topic(BaseModel):
    community_id: str
    user_id: str
    topic_id : str
    title: str
    content: str
    image_url: str
    is_approved: bool 
    total_comments: int
    created_at: str
    updated_at:str


class PostTopic(BaseModel):
    title : str
    content : str
    image_url : str


class UpdateTopic(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None


class Comment(BaseModel):
    topic_id :str
    user_id: str
    comment_id: str
    content: str
    image_url: str
    created_at: str
    updated_at:str


class AddComment(BaseModel):
    content: str
    image_url :str


class UpdateComment(BaseModel):
    content: Optional[str] = None
    image_url: Optional[str] = None
    