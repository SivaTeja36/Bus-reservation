from datetime import datetime
from pydantic import (
    BaseModel, 
    EmailStr
)

from app.models.bus_models import GetBusResponse
from app.models.company_models import GetCompanyResponse


class TicketRequest(BaseModel):
    bus_id: int 
    seat_number: int 
    passenger_name: str
    passenger_contact: str 
    passenger_email: EmailStr 
    status: str 


class TicketResponse(BaseModel):
    message: str


class GetTicketResponse(BaseModel):
    id: int 
    seat_number: int 
    passenger_name: str
    passenger_contact: str 
    passenger_email: str 
    status: str 
    created_at: datetime 
    updated_at: datetime  
    bus_data: GetBusResponse
    company_data: GetCompanyResponse