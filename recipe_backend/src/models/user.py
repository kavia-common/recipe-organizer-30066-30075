"""
User model.
"""

from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    # Only for type checkers; avoids import cycles at runtime
    from .recipe import Recipe  # noqa: F401
    from .saved_recipe import SavedRecipe  # noqa: F401


class User(Base):
    """Represents an application user."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    recipes: Mapped[List["Recipe"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    saved_recipes: Mapped[List["SavedRecipe"]] = relationship(back_populates="user", cascade="all, delete-orphan")
