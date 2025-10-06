from pydantic import BaseModel, Field


class Pagination(BaseModel):
    limit: int = Field(10, description="Max items to return")
    offset: int = Field(0, description="Items to skip before starting to collect the result set")


class PaginatedResponse(BaseModel):
    total: int = Field(..., description="Total matching items")
    limit: int = Field(..., description="Requested page size")
    offset: int = Field(..., description="Requested offset")
