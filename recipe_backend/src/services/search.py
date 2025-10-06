from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from src.models.recipe import Recipe
from src.models.recipe_tag import RecipeTag


# PUBLIC_INTERFACE
def search_recipes(
    db: Session,
    *,
    query: str | None,
    category_id: int | None,
    tag_ids: list[int],
    limit: int,
    offset: int,
) -> tuple[list[Recipe], int]:
    """Search recipes by query, category, and tags with pagination."""
    stmt = select(Recipe).options(
        joinedload(Recipe.category),
        joinedload(Recipe.tags),
    )

    # Apply filters
    if query:
        like_q = f"%{query.lower()}%"
        stmt = stmt.where(
            func.lower(Recipe.title).like(like_q) | func.lower(Recipe.description).like(like_q)
        )
    if category_id:
        stmt = stmt.where(Recipe.category_id == category_id)
    if tag_ids:
        # filter recipes that have all the specified tags
        for tid in tag_ids:
            stmt = stmt.where(
                Recipe.id.in_(
                    select(RecipeTag.recipe_id).where(RecipeTag.tag_id == tid)
                )
            )

    # Count total
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.scalar(count_stmt) or 0

    # Pagination and ordering
    stmt = stmt.order_by(Recipe.created_at.desc()).limit(limit).offset(offset)

    items = db.scalars(stmt).all()
    return items, total
