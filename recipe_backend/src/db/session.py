"""
Database engine and session management.

Provides a synchronous SQLAlchemy Engine and a scoped SessionLocal for request handling.
Defaults to SQLite for development, switchable via DATABASE_URL env var (e.g., Postgres).
"""

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.core.config import get_settings
from src.db.base import Base


settings = get_settings()

# SQLite needs check_same_thread=False for multi-threaded FastAPI servers
engine_kwargs = {}
if settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, **engine_kwargs)

# Factory for sessions (autocommit/flush disabled for explicit control)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# PUBLIC_INTERFACE
def init_db(create_all_in_dev: bool = True) -> None:
    """Initialize database. In development, optionally create tables if they do not exist."""
    if create_all_in_dev and settings.ENV.lower() in {"dev", "development"}:
        Base.metadata.create_all(bind=engine)


@contextmanager
# PUBLIC_INTERFACE
def get_db() -> Iterator[Session]:
    """Yield a database session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
