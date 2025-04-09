
from typing import Optional
from pydantic import (
    BaseModel, 
    EmailStr
)


class LoginRequest(BaseModel):
    userName: EmailStr
    password: str


class LoginResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    contact: str