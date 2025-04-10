import os
from dotenv import load_dotenv

from fastapi import (
    HTTPException, 
    Request
)
from jose import jwt

from app.models.user_models import CurrentContextUser
from app.utils.constants import AUTHORIZATION

load_dotenv()

SECRET_KEY: str = os.getenv("JWT_SECRET")  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300  # 3 hours


def __verify_jwt(token: str):
    token = token.replace("Bearer ", "")
    payload = jwt.decode(
        token, 
        SECRET_KEY, 
        algorithms=[ALGORITHM], 
        options={"verify_sub": True}
    )  
    user = payload.get("sub")
    
    if user:
        cur_user = CurrentContextUser()
        cur_user.name = payload.get("name")
        cur_user.email = str(user)
        cur_user.role = payload.get("role")
        cur_user.branch_id = payload.get("branch_id")
        return cur_user


async def verify_auth_token(request: Request):
    """
        Verify the authentication token in the request headers.
    """
    non_authenticated_paths = {"login", "refresh"}
    protected_paths = {
        "admin", "companies", "buses", 
        "tickets"
    }
    
    if not any(path in request.url.path for path in non_authenticated_paths) and any(
        path in request.url.path for path in protected_paths
    ):
        auth: str = request.headers.get(AUTHORIZATION) or ""
        
        try:
            request.state.user = __verify_jwt(token=auth)
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail=str(e)
            )
