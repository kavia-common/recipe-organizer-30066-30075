from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.api.deps import get_current_user, get_db_dep
from src.models.tag import Tag
from src.models.category import Category
from src.schemas.taxonomy import TagCreate, TagPublic, CategoryCreate, CategoryPublic

router = APIRouter(tags=["taxonomy"])


@router.post("/taxonomy/tags", response_model=TagPublic, status_code=status.HTTP_201_CREATED, summary="Create tag")
def create_tag(payload: TagCreate, db: Session = Depends(get_db_dep), _user=Depends(get_current_user)) -> TagPublic:
    """
    Create a new tag (auth required).
    """
    existing = db.query(Tag).filter(Tag.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag already exists")
    tag = Tag(name=payload.name)
    db.add(tag)
    db.flush()
    db.refresh(tag)
    return tag


@router.get("/taxonomy/tags", response_model=list[TagPublic], summary="List tags")
def list_tags(db: Session = Depends(get_db_dep)) -> list[TagPublic]:
    """
    List all tags.
    """
    return db.scalars(select(Tag).order_by(Tag.name.asc())).all()


@router.post("/taxonomy/categories", response_model=CategoryPublic, status_code=status.HTTP_201_CREATED, summary="Create category")
def create_category(payload: CategoryCreate, db: Session = Depends(get_db_dep), _user=Depends(get_current_user)) -> CategoryPublic:
    """
    Create a new category (auth required).
    """
    existing = db.query(Category).filter(Category.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")
    category = Category(name=payload.name, description=payload.description)
    db.add(category)
    db.flush()
    db.refresh(category)
    return category


@router.get("/taxonomy/categories", response_model=list[CategoryPublic], summary="List categories")
def list_categories(db: Session = Depends(get_db_dep)) -> list[CategoryPublic]:
    """
    List all categories.
    """
    return db.scalars(select(Category).order_by(Category.name.asc())).all()
