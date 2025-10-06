from typing import List, Optional

from pydantic import BaseModel, Field

from src.schemas.recipe import RecipePublic
from src.schemas.common import PaginatedResponse


class SearchFilters(BaseModel):
    category_id: Optional[int] = Field(default=None, description="Filter by category id")
    tag_ids: List[int] = Field(default_factory=list, description="Filter by tag ids")


class SearchResponse(PaginatedResponse):
    items: List[RecipePublic] = Field(default_factory=list, description="Matching recipes")
