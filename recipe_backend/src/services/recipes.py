from typing import List, Optional, Tuple

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func

from src.models.recipe import Recipe
from src.models.tag import Tag


def _apply_recipe_relations(stmt):
    """Utility to eager-load category and tags."""
    return stmt.options(
        joinedload(Recipe.category),
        joinedload(Recipe.tags),
    )


# PUBLIC_INTERFACE
def create_recipe(
    db: Session,
    *,
    author_id: int,
    title: str,
    description: Optional[str],
    instructions: str,
    ingredients: str,
    category_id: Optional[int],
    tag_ids: List[int],
) -> Recipe:
    """Create a recipe and attach tags."""
    recipe = Recipe(
        title=title,
        description=description,
        instructions=instructions,
        ingredients=ingredients,
        author_id=author_id,
        category_id=category_id,
    )
    if tag_ids:
        tags = db.scalars(select(Tag).where(Tag.id.in_(tag_ids))).all()
        recipe.tags = list(tags)
    db.add(recipe)
    db.flush()
    db.refresh(recipe)
    return recipe


# PUBLIC_INTERFACE
def get_recipe(db: Session, recipe_id: int) -> Optional[Recipe]:
    """Return a recipe by id with relations."""
    stmt = _apply_recipe_relations(select(Recipe).where(Recipe.id == recipe_id))
    return db.scalars(stmt).first()


# PUBLIC_INTERFACE
def list_recipes(db: Session, *, limit: int = 10, offset: int = 0) -> Tuple[List[Recipe], int]:
    """List recipes paginated."""
    total = db.scalar(select(func.count()).select_from(Recipe)) or 0
    stmt = _apply_recipe_relations(select(Recipe).order_by(Recipe.created_at.desc()).limit(limit).offset(offset))
    items = db.scalars(stmt).all()
    return items, total


# PUBLIC_INTERFACE
def update_recipe(
    db: Session,
    *,
    recipe: Recipe,
    title: Optional[str] = None,
    description: Optional[str] = None,
    instructions: Optional[str] = None,
    ingredients: Optional[str] = None,
    category_id: Optional[int] = None,
    tag_ids: Optional[List[int]] = None,
) -> Recipe:
    """Update a recipe and its tags if provided."""
    if title is not None:
        recipe.title = title
    if description is not None:
        recipe.description = description
    if instructions is not None:
        recipe.instructions = instructions
    if ingredients is not None:
        recipe.ingredients = ingredients
    if category_id is not None:
        recipe.category_id = category_id
    if tag_ids is not None:
        tags = db.scalars(select(Tag).where(Tag.id.in_(tag_ids))).all() if tag_ids else []
        recipe.tags = list(tags)
    db.add(recipe)
    db.flush()
    db.refresh(recipe)
    return recipe


# PUBLIC_INTERFACE
def delete_recipe(db: Session, *, recipe: Recipe) -> None:
    """Delete a recipe."""
    db.delete(recipe)
    db.flush()
