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

class CreateUser(User):
    pass

class ReadUser(User):
    user_id : int

class UserUpdate(User):
    first_name : Optional[str] =None
    last_name:Optional[str] =None
    email :Optional[str] =None
    password : Optional[str] =None

    class config:
        orm_mode = True 