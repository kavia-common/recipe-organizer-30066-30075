"""
Category model.
"""

from typing import List, TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from .recipe import Recipe  # noqa: F401


class Category(Base):
    """Represents a recipe category."""
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    recipes: Mapped[List["Recipe"]] = relationship(back_populates="category")
