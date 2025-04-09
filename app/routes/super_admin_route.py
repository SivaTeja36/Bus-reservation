from automapper import mapper
from fastapi import (
    APIRouter, 
    Depends,
    status
)

from app.models.base_response_model import ApiResponse
from app.models.branch_models import (
    BranchRequest, 
    BranchResponse
)
from app.models.user_models import (
    UserCreationRequest, 
    UserCreationResponse
)
from app.services.branch_service import BranchService
from app.services.user_service import UserService

router = APIRouter(prefix="/admin", tags=["BRANCH MANAGEMENT SERVICE"])


@router.post(
    "/branch",
    response_model=ApiResponse[BranchRequest],
    status_code=status.HTTP_201_CREATED,
)
async def create_organization(
    request: BranchRequest, 
    service: BranchService = Depends(BranchService)
) -> ApiResponse[BranchResponse]:
    return ApiResponse(data=service.create_branch(request))


@router.get(
    "/branch/{id}", 
    response_model=ApiResponse[BranchResponse], 
    status_code=status.HTTP_200_OK
)
async def get_organization(
    id: int, 
    service: BranchService = Depends(BranchService)
) -> ApiResponse[BranchResponse]:
    return ApiResponse(data=service.get_branch(id))


@router.post(
    "/user", 
    response_model=UserCreationResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    request: UserCreationRequest, 
    service: UserService = Depends(UserService)
) -> UserCreationResponse:
    user = service.create_user(
        request.name,
        request.username,
        request.password,
        request.role,
        request.contact,
    )
    return mapper.to(UserCreationResponse).map(user)
