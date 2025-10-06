from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    name: str = Field(..., description="Tag name")


class TagPublic(BaseModel):
    id: int = Field(..., description="Tag ID")
    name: str = Field(..., description="Tag name")

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str = Field(..., description="Category name")
    description: str | None = Field(default=None, description="Category description")


class CategoryPublic(BaseModel):
    id: int = Field(..., description="Category ID")
    name: str = Field(..., description="Category name")
    description: str | None = Field(default=None, description="Category description")

    class Config:
        from_attributes = True
