from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.deps import get_db_dep
from src.core.security import hash_password, verify_password, create_access_token
from src.models.user import User
from src.schemas.auth import RegisterRequest, LoginRequest, Token

router = APIRouter(tags=["auth"])


@router.post("/auth/register", response_model=Token, summary="Register a new user", description="Create a new user and receive an access token.")
def register(payload: RegisterRequest, db: Session = Depends(get_db_dep)) -> Token:
    """
    Register a new user.

    Parameters:
    - payload: RegisterRequest containing email, password, and optional full_name.

    Returns:
    - Token: JWT access token to authenticate subsequent requests.
    """
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(email=payload.email, hashed_password=hash_password(payload.password), full_name=payload.full_name)
    db.add(user)
    db.flush()
    db.refresh(user)
    token = create_access_token(user.id)
    return Token(access_token=token, token_type="bearer")


@router.post("/auth/login", response_model=Token, summary="Login", description="Authenticate using email and password to receive an access token.")
def login(payload: LoginRequest, db: Session = Depends(get_db_dep)) -> Token:
    """
    Login endpoint.

    Parameters:
    - payload: LoginRequest with email and password.

    Returns:
    - Token: JWT access token on successful authentication.
    """
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    token = create_access_token(user.id)
    return Token(access_token=token, token_type="bearer")
