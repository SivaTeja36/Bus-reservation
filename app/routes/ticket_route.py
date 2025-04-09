from typing import List
from fastapi import (
    APIRouter, 
    Depends,
    status
)
from pydantic import PositiveInt

from app.models.base_response_model import ApiResponse
from app.models.ticket_models import (
    TicketRequest,
    TicketResponse,
    GetTicketResponse
)
from app.services.ticket_service import TicketService

router = APIRouter(
    prefix="/buses", 
    tags=["TICKET MANAGEMENT SERVICE"]
)


@router.post(
    "",
    response_model=ApiResponse[TicketResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_ticket(
    request: TicketRequest, 
    service: TicketService = Depends(TicketService)
) -> ApiResponse[TicketResponse]:
    return ApiResponse(data=service.create_ticket(request))


@router.get(
    "",
    response_model=ApiResponse[List[GetTicketResponse]],
    status_code=status.HTTP_200_OK,
)
async def get_all_tickets( 
    service: TicketService = Depends(TicketService)
) -> ApiResponse[List[GetTicketResponse]]:
    return ApiResponse(data=service.get_all_tickets())


@router.get(
    "{id}",
    response_model=ApiResponse[GetTicketResponse],
    status_code=status.HTTP_200_OK
)
async def get_ticket_by_id(
    id: PositiveInt, 
    service: TicketService = Depends(TicketService)
) -> ApiResponse[GetTicketResponse]:
    return ApiResponse(data=service.get_ticket_by_id(id))


@router.put(
    "{id}",
    response_model=ApiResponse[TicketResponse],
    status_code=status.HTTP_200_OK
)
async def update_ticket_by_id(
    id: PositiveInt, 
    request: TicketRequest, 
    service: TicketService = Depends(TicketService)
) -> ApiResponse[TicketResponse]:
    return ApiResponse(data=service.update_ticket_by_id(id, request))


@router.delete(
    "{id}",
    response_model=ApiResponse[TicketResponse],
    status_code=status.HTTP_200_OK
)   
async def delete_ticket_by_id(
    id: PositiveInt, 
    service: TicketService = Depends(TicketService)
) -> ApiResponse[TicketResponse]:
    return ApiResponse(data=service.delete_ticket_by_id(id))