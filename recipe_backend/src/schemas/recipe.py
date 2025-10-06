from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from src.schemas.taxonomy import TagPublic, CategoryPublic


class RecipeBase(BaseModel):
    title: str = Field(..., description="Recipe title")
    description: Optional[str] = Field(default=None, description="Short description")
    instructions: str = Field(..., description="Recipe instructions")
    ingredients: str = Field(..., description="Recipe ingredients")
    category_id: Optional[int] = Field(default=None, description="Category reference")
    tag_ids: List[int] = Field(default_factory=list, description="List of tag IDs")


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(default=None, description="Recipe title")
    description: Optional[str] = Field(default=None, description="Short description")
    instructions: Optional[str] = Field(default=None, description="Recipe instructions")
    ingredients: Optional[str] = Field(default=None, description="Recipe ingredients")
    category_id: Optional[int] = Field(default=None, description="Category reference")
    tag_ids: Optional[List[int]] = Field(default=None, description="List of tag IDs")


class RecipePublic(BaseModel):
    id: int = Field(..., description="Recipe ID")
    title: str = Field(..., description="Recipe title")
    description: Optional[str] = Field(default=None, description="Short description")
    instructions: str = Field(..., description="Recipe instructions")
    ingredients: str = Field(..., description="Recipe ingredients")
    category: Optional[CategoryPublic] = Field(default=None, description="Category")
    tags: List[TagPublic] = Field(default_factory=list, description="Tags")
    author_id: int = Field(..., description="Author user ID")
    created_at: datetime = Field(..., description="Created timestamp")
    updated_at: datetime = Field(..., description="Updated timestamp")

    class Config:
        from_attributes = True
