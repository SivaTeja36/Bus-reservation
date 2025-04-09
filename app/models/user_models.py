from datetime import datetime
from typing import Optional
from pydantic import (
    BaseModel, 
    EmailStr,
    PositiveInt
)

class UserCreationRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    contact: str
    branch_id: PositiveInt


class UserCreationResponse(BaseModel):
    message: str
    

class CurrentContextUser():
    username: str
    name: str
    role: str