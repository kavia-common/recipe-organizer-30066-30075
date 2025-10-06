"""
Recipe model.
"""

from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .category import Category  # noqa: F401
    from .tag import Tag  # noqa: F401
    from .saved_recipe import SavedRecipe  # noqa: F401


class Recipe(Base):
    """Represents a recipe created by a user."""
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    instructions: Mapped[str] = mapped_column(Text, nullable=False)
    ingredients: Mapped[str] = mapped_column(Text, nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    author: Mapped["User"] = relationship(back_populates="recipes")
    category: Mapped[Optional["Category"]] = relationship(back_populates="recipes")
    tags: Mapped[List["Tag"]] = relationship(
        secondary="recipe_tags",
        back_populates="recipes",
    )
    saved_by: Mapped[List["SavedRecipe"]] = relationship(back_populates="recipe", cascade="all, delete-orphan")
