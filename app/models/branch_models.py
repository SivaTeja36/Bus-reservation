from pydantic import BaseModel


class BranchRequest(BaseModel):
    name: str
    logo: str


class BranchResponse(BaseModel):
    id: int
    name: str
    city: str
    access_key: str