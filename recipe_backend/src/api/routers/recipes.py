from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.api.deps import get_current_user, get_db_dep
from src.models.user import User
from src.schemas.recipe import RecipeCreate, RecipePublic, RecipeUpdate
from src.services.recipes import create_recipe, get_recipe, list_recipes, update_recipe, delete_recipe

router = APIRouter(tags=["recipes"])


@router.post("/recipes", response_model=RecipePublic, status_code=status.HTTP_201_CREATED, summary="Create a recipe")
def create_recipe_endpoint(
    payload: RecipeCreate,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_user),
) -> RecipePublic:
    """
    Create a new recipe owned by the authenticated user.
    """
    recipe = create_recipe(
        db,
        author_id=current_user.id,
        title=payload.title,
        description=payload.description,
        instructions=payload.instructions,
        ingredients=payload.ingredients,
        category_id=payload.category_id,
        tag_ids=payload.tag_ids,
    )
    return recipe


@router.get("/recipes/{recipe_id}", response_model=RecipePublic, summary="Get a recipe by ID")
def get_recipe_endpoint(recipe_id: int, db: Session = Depends(get_db_dep)) -> RecipePublic:
    """
    Retrieve a recipe by its ID.
    """
    recipe = get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe


@router.get("/recipes", response_model=dict, summary="List recipes with pagination")
def list_recipes_endpoint(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db_dep),
) -> dict:
    """
    List recipes with pagination support.
    """
    items, total = list_recipes(db, limit=limit, offset=offset)
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items,
    }


@router.patch("/recipes/{recipe_id}", response_model=RecipePublic, summary="Update a recipe (owner only)")
def update_recipe_endpoint(
    recipe_id: int,
    payload: RecipeUpdate,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_user),
) -> RecipePublic:
    """
    Update fields of a recipe owned by the current user.
    """
    recipe = get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    if recipe.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this recipe")
    updated = update_recipe(
        db,
        recipe=recipe,
        title=payload.title,
        description=payload.description,
        instructions=payload.instructions,
        ingredients=payload.ingredients,
        category_id=payload.category_id,
        tag_ids=payload.tag_ids,
    )
    return updated


@router.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a recipe (owner only)")
def delete_recipe_endpoint(
    recipe_id: int,
    db: Session = Depends(get_db_dep),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete a recipe owned by the current user.
    """
    recipe = get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    if recipe.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this recipe")
    delete_recipe(db, recipe=recipe)
    return None
