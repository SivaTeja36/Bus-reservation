from pydantic import (
    BaseModel, 
    EmailStr
)


class CompanyRequest(BaseModel):
    name: str 
    contact_person_name: str
    email: EmailStr
    address: str 
    phone_number: str 


class CompanyResponse(BaseModel):
    message: str


class GetCompanyResponse(BaseModel):
    id: int
    name: str 
    contact_person_name: str
    email: EmailStr
    address: str 
    phone_number: str 
    created_at: str
    updated_at: str
    is_active: bool