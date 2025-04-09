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
    

class CurrentContextUser():
    name: str
    email: str
    role: str
    branch_id: int