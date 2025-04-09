from datetime import datetime
from typing import Optional
from pydantic import (
    BaseModel, 
    EmailStr
)

class UserCreationRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    contact: str
    branch_id: Optional[int] = None


class UserCreationResponse(BaseModel):
    id: int
    name: str 
    username: str 
    contact: str
    role: str
    created_at: datetime
    is_active: bool
    

class CurrentContextUser():
    username: str
    name: str
    role: str