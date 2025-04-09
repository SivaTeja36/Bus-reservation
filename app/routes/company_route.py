from fastapi import (
    APIRouter, 
    Depends,
    status
)
from pydantic import PositiveInt

from app.models.base_response_model import ApiResponse
from app.models.company_models import (
    CompanyRequest,
    CompanyResponse,
    GetCompanyResponse
)
from app.services.company_service import CompanyService

router = APIRouter(
    prefix="/companies", 
    tags=["COMPANY MANAGEMENT SERVICE"]
)


@router.post(
    "",
    response_model=ApiResponse[CompanyResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_organization(
    request: CompanyRequest, 
    service: CompanyService = Depends(CompanyService)
) -> ApiResponse[CompanyResponse]:
    return ApiResponse(data=service.create_company(request))


@router.get(
    "{id}",
    response_model=ApiResponse[GetCompanyResponse],
    status_code=status.HTTP_200_OK
)
async def get_company_by_id(
    id: PositiveInt, 
    service: CompanyService = Depends(CompanyService)
) -> ApiResponse[GetCompanyResponse]:
    return ApiResponse(data=service.get_company_by_id(id))


@router.put(
    "{id}",
    response_model=ApiResponse[CompanyResponse],
    status_code=status.HTTP_200_OK
)
async def update_company_by_id(
    id: PositiveInt, 
    request: CompanyRequest, 
    service: CompanyService = Depends(CompanyService)
) -> ApiResponse[CompanyResponse]:
    return ApiResponse(data=service.update_company_by_id(id, request))


@router.delete(
    "{id}",
    response_model=ApiResponse[CompanyResponse],
    status_code=status.HTTP_200_OK
)   
async def delete_company_by_id(
    id: PositiveInt, 
    service: CompanyService = Depends(CompanyService)
) -> ApiResponse[CompanyResponse]:
    return ApiResponse(data=service.delete_company_by_id(id))