"""
SQLAlchemy Base and model registry.

This module defines the declarative Base and ensures models are imported
so that Base.metadata.create_all() can discover them.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""
    pass


# Import models here so Alembic/autocreation can see them
# These imports are intentionally unused but register models with Base.
# pylint: disable=unused-import, wrong-import-position
from src.models import user as _user  # noqa: F401
from src.models import category as _category  # noqa: F401
from src.models import tag as _tag  # noqa: F401
from src.models import recipe as _recipe  # noqa: F401
from src.models import recipe_tag as _recipe_tag  # noqa: F401
from src.models import saved_recipe as _saved_recipe  # noqa: F401
