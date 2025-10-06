"""
Core configuration for the backend application.

Loads environment variables and exposes settings for use across the app.
Uses python-dotenv via FastAPI/uvicorn support to load .env in development.

Do not hardcode secrets; request values to be provided via the .env file.
"""

from pydantic import BaseModel
import os


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    # Default to local SQLite database in project root for development
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./recipes.db")
    ENV: str = os.getenv("ENV", "development")

    # JWT and security related
    JWT_SECRET_KEY: str | None = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # CORS
    FRONTEND_ORIGIN: str | None = os.getenv("FRONTEND_ORIGIN")
    SITE_URL: str | None = os.getenv("SITE_URL")


# PUBLIC_INTERFACE
def get_settings() -> Settings:
    """Return application settings loaded from environment variables."""
    return Settings()
