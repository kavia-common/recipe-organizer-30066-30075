from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_current_user, get_db_dep
from src.core.security import hash_password
from src.models.user import User
from src.schemas.user import UserPublic, UserUpdate

router = APIRouter(tags=["users"])


@router.get("/users/me", response_model=UserPublic, summary="Get current user")
def get_me(current_user: User = Depends(get_current_user)) -> UserPublic:
    """
    Get the current authenticated user's profile.
    """
    return current_user  # pydantic from_attributes will exclude hashed_password by design


@router.patch("/users/me", response_model=UserPublic, summary="Update current user")
def update_me(update: UserUpdate, db: Session = Depends(get_db_dep), current_user: User = Depends(get_current_user)) -> UserPublic:
    """
    Update the current user's profile details. Supports updating full_name and password.
    """
    if update.full_name is not None:
        current_user.full_name = update.full_name
    if update.password is not None and update.password.strip():
        current_user.hashed_password = hash_password(update.password)
    db.add(current_user)
    db.flush()
    db.refresh(current_user)
    return current_user
