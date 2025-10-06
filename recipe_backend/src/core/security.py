from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from src.core.config import get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTSettings:
    """Encapsulates JWT settings loaded from environment variables."""
    def __init__(self) -> None:
        settings = get_settings()
        # These must be provided via environment variables in production
        self.secret_key: str = getattr(settings, "JWT_SECRET_KEY", None) or "dev-secret-change-me"
        self.algorithm: str = getattr(settings, "JWT_ALGORITHM", "HS256")
        # Default token expiry 60 minutes
        self.access_token_expire_minutes: int = int(getattr(settings, "JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60))


jwt_settings = JWTSettings()


# PUBLIC_INTERFACE
def hash_password(plain_password: str) -> str:
    """Hash a plain text password using bcrypt."""
    return pwd_context.hash(plain_password)


# PUBLIC_INTERFACE
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


# PUBLIC_INTERFACE
def create_access_token(subject: str | int, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token for the given subject (user id or email)."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=jwt_settings.access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": str(subject), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, jwt_settings.secret_key, algorithm=jwt_settings.algorithm)
    return encoded_jwt


# PUBLIC_INTERFACE
def decode_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token, returning the payload if valid, else None."""
    try:
        payload = jwt.decode(token, jwt_settings.secret_key, algorithms=[jwt_settings.algorithm])
        return payload
    except JWTError:
        return None
