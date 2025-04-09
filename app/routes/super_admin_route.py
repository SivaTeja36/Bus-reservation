from typing import List

from fastapi import (
    APIRouter, 
    Depends,
    status
)

from app.models.base_response_model import ApiResponse
from app.models.branch_models import (
    BranchRequest, 
    BranchResponse,
    GetBranchResponse
)
from app.models.user_models import (
    UserCreationRequest, 
    UserCreationResponse
)
from app.services.branch_service import BranchService
from app.services.user_service import UserService

router = APIRouter(prefix="/admin", tags=["BRANCH MANAGEMENT SERVICE"])


@router.post(
    "/branches",
    response_model=ApiResponse[BranchResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_organization(
    request: BranchRequest, 
    service: BranchService = Depends(BranchService)
) -> ApiResponse[BranchResponse]:
    return ApiResponse(data=service.create_branch(request))


@router.get(
    "/branches", 
    response_model=ApiResponse[List[GetBranchResponse]], 
    status_code=status.HTTP_200_OK
)
async def get_organization(
    service: BranchService = Depends(BranchService)
) -> ApiResponse[List[GetBranchResponse]]:
    return ApiResponse(data=service.get_all_branch())


@router.get(
    "/branches/{id}", 
    response_model=ApiResponse[GetBranchResponse], 
    status_code=status.HTTP_200_OK
)
async def get_organization(
    id: int, 
    service: BranchService = Depends(BranchService)
) -> ApiResponse[GetBranchResponse]:
    return ApiResponse(data=service.get_branch(id))


@router.post(
    "/users", 
    response_model=ApiResponse[UserCreationResponse], 
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    request: UserCreationRequest, 
    service: UserService = Depends(UserService)
) -> ApiResponse[UserCreationResponse]:
    return ApiResponse(data=service.create_user(request))
