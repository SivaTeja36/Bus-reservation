from fastapi import (
    APIRouter, 
    Depends,
    status
)
from pydantic import PositiveInt

from app.models.base_response_model import ApiResponse
from app.models.bus_models import (
    BusRequest,
    BusResponse,
    GetBusResponse
)
from app.services.bus_service import BusService

router = APIRouter(
    prefix="/buses", 
    tags=["BUS MANAGEMENT SERVICE"]
)


@router.post(
    "",
    response_model=ApiResponse[BusResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_bus(
    request: BusRequest, 
    service: BusService = Depends(BusService)
) -> ApiResponse[BusResponse]:
    return ApiResponse(data=service.create_bus(request))


@router.get(
    "",
    response_model=ApiResponse[BusResponse],
    status_code=status.HTTP_201_CREATED,
)
async def get_all_buses( 
    service: BusService = Depends(BusService)
) -> ApiResponse[BusResponse]:
    return ApiResponse(data=service.get_all_buses())


@router.get(
    "{id}",
    response_model=ApiResponse[GetBusResponse],
    status_code=status.HTTP_200_OK
)
async def get_bus_by_id(
    id: PositiveInt, 
    service: BusService = Depends(BusService)
) -> ApiResponse[GetBusResponse]:
    return ApiResponse(data=service.get_bus_by_id(id))


@router.put(
    "{id}",
    response_model=ApiResponse[BusResponse],
    status_code=status.HTTP_200_OK
)
async def update_bus_by_id(
    id: PositiveInt, 
    request: BusRequest, 
    service: BusService = Depends(BusService)
) -> ApiResponse[BusResponse]:
    return ApiResponse(data=service.update_bus_by_id(id, request))


@router.delete(
    "{id}",
    response_model=ApiResponse[BusResponse],
    status_code=status.HTTP_200_OK
)   
async def delete_bus_by_id(
    id: PositiveInt, 
    service: BusService = Depends(BusService)
) -> ApiResponse[BusResponse]:
    return ApiResponse(data=service.delete_bus_by_id(id))