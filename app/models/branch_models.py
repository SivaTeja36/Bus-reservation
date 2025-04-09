from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BranchRequest(BaseModel):
    city: str
    domain_name: str
    logo: Optional[str] = None


class BranchResponse(BaseModel):
    message: str


class GetBranchResponse(BaseModel):
    id: int
    city: str
    domain_name: str
    logo_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool