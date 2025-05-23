from typing import List

from fastapi import (
    APIRouter, 
    Depends,
    Request,
    status
)

from app.models.base_response_model import ApiResponse
from app.models.branch_models import (
    BranchRequest, 
    BranchResponse,
    GetBranchResponse
)
from app.models.user_models import (
    GetUserResponse,
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
async def create_branch(
    request: BranchRequest, 
    service: BranchService = Depends(BranchService)
) -> ApiResponse[BranchResponse]:
    return ApiResponse(data=service.create_branch(request))


@router.get(
    "/branches", 
    response_model=ApiResponse[List[GetBranchResponse]], 
    status_code=status.HTTP_200_OK
)
async def get_all_branches(
    service: BranchService = Depends(BranchService)
) -> ApiResponse[List[GetBranchResponse]]:
    return ApiResponse(data=service.get_all_branches())


@router.get(
    "/branches/{id}", 
    response_model=ApiResponse[GetBranchResponse], 
    status_code=status.HTTP_200_OK
)
async def get_branch_by_id(
    id: int, 
    service: BranchService = Depends(BranchService)
) -> ApiResponse[GetBranchResponse]:
    return ApiResponse(data=service.get_branch_by_id(id))


@router.put(
    "/branches/{id}", 
    response_model=ApiResponse[BranchResponse], 
    status_code=status.HTTP_200_OK
)
async def update_branch_by_id(
    id: int, 
    request: BranchRequest, 
    service: BranchService = Depends(BranchService)
) -> ApiResponse[BranchResponse]:
    return ApiResponse(data=service.update_branch_by_id(id, request))


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


@router.get(
    "/users", 
    response_model=ApiResponse[List[GetUserResponse]], 
    status_code=status.HTTP_201_CREATED
)
async def get_all_users(
    request_state: Request, 
    service: UserService = Depends(UserService)
) -> ApiResponse[List[GetUserResponse]]:
    branch_id = request_state.state.user.branch_id
    return ApiResponse(data=service.get_all_users(branch_id))
