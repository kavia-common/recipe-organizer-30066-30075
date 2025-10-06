"""
Tag model.
"""

from typing import List, TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from .recipe import Recipe  # noqa: F401


class Tag(Base):
    """Represents a tag used to classify recipes."""
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    recipes: Mapped[List["Recipe"]] = relationship(
        secondary="recipe_tags",
        back_populates="tags",
    )
