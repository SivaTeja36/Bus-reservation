
from typing import Optional
from pydantic import (
    BaseModel, 
    EmailStr
)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    name: str
    email: EmailStr
    role: str
    contact: str