from datetime import datetime
from pydantic import (
    BaseModel, 
    PositiveInt
)

from app.models.company_models import GetCompanyResponse
from app.utils.enums import BusTypeEnum


class BusRequest(BaseModel):
    company_id: PositiveInt 
    bus_number: str 
    bus_type: BusTypeEnum 
    total_seats: PositiveInt


class BusResponse(BaseModel):
    message: str


class GetBusResponse(BaseModel):
    id: int
    company_id: int
    bus_number: str
    bus_type: str
    total_seats: int
    created_at: datetime
    is_active: bool
    company_data: GetCompanyResponse


class BusScheduleRequest(BaseModel):
    bus_id: PositiveInt
    route_id: PositiveInt
    departure_time: datetime
    arrival_time: datetime    