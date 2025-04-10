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


class GetRouteResponse(BaseModel):
    id: int 
    stops: list[str]
    source: str 
    destination: str 
    created_at: datetime 


class BusScheduleRequest(BaseModel):
    bus_id: PositiveInt
    route_id: PositiveInt
    departure_time: datetime
    arrival_time: datetime    


class GetBusScheduleResponse(BaseModel):
    id: int
    bus_id: int 
    route_id: int 
    departure_time: datetime 
    arrival_time: datetime 
    created_at: datetime
    updated_at: datetime
    bus_data: GetBusResponse
    route_data: GetRouteResponse