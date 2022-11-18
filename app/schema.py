from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional 

class UserSignInRequest(BaseModel):
    username: str
    firstname: str
    lastname: str
    password: str
    email: str
    imageURL: str

class UserSignInResponse(BaseModel):
    pass

class ChangePasswordRequest(BaseModel):
    pass 
class ForgotPassword(BaseModel):
    pass 
