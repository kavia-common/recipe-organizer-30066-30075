"""
SavedRecipe model representing a user's saved (favorite) recipes.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .recipe import Recipe  # noqa: F401


class SavedRecipe(Base):
    """A favorite relationship between a user and a recipe."""
    __tablename__ = "saved_recipes"
    __table_args__ = (
        UniqueConstraint("user_id", "recipe_id", name="uq_user_recipe_saved"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"), index=True, nullable=False)
    saved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="saved_recipes")
    recipe: Mapped["Recipe"] = relationship(back_populates="saved_by")
