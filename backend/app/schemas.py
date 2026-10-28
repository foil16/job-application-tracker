from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, AfterValidator
from datetime import datetime


def lowercase_email(email:str) -> str:
        return email.lower()
email_type = Annotated[EmailStr,AfterValidator(lowercase_email)]

class RegisterRequest(BaseModel):
    email: email_type
    password : str = Field(...,min_length = 8)

class LoginRequest(BaseModel):
    email: email_type
    password : str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: email_type
    created_at :datetime