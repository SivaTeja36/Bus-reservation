from pydantic import BaseModel


class BranchRequest(BaseModel):
    name: str
    city: str
    domain_name: str
    logo: str


class BranchResponse(BaseModel):
    message: str