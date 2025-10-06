from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.api.deps import get_db_dep
from src.services.search import search_recipes

router = APIRouter(tags=["search"])


@router.get("/search", response_model=dict, summary="Search recipes")
def search(
    q: str | None = Query(default=None, description="Search query"),
    category_id: int | None = Query(default=None, description="Filter by category id"),
    tag_ids: list[int] = Query(default_factory=list, description="List of tag ids to filter"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db_dep),
) -> dict:
    """
    Search recipes with optional query string, category, and tags. Supports pagination via limit/offset.
    """
    items, total = search_recipes(db, query=q, category_id=category_id, tag_ids=tag_ids, limit=limit, offset=offset)
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items,
    }
