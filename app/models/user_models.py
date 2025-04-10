from datetime import datetime
from pydantic import (
    BaseModel, 
    EmailStr,
    PositiveInt,
    Field,
    validator
)

from app.utils.validators import validate_password

class UserCreationRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=16)
    role: str
    contact: str
    branch_id: PositiveInt

    @validator("password")
    def validate_set_password(cls, password: str):
        return validate_password(password)


class UserCreationResponse(BaseModel):
    message: str


class GetUserResponse(BaseModel):
    id: int 
    name: str 
    email: str 
    contact: str 
    role: str
    branch_id: int 
    created_at: datetime 
    updated_at: datetime 
    is_active: bool 
    

class CurrentContextUser():
    name: str
    email: str
    role: str
    branch_id: int