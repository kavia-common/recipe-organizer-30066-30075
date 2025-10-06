from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.models.user import User
from src.core.security import decode_token

# OAuth2PasswordBearer expects a tokenUrl for the OpenAPI docs "Authorize" flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# PUBLIC_INTERFACE
def get_db_dep() -> Generator[Session, None, None]:
    """FastAPI dependency providing a SQLAlchemy session."""
    with get_db() as db:
        yield db


# PUBLIC_INTERFACE
def get_current_user(db: Session = Depends(get_db_dep), token: str = Depends(oauth2_scheme)) -> User:
    """Retrieve the current authenticated user using a Bearer token."""
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user_id: Optional[int] = int(payload["sub"]) if str(payload["sub"]).isdigit() else None
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive or missing user")
    return user
