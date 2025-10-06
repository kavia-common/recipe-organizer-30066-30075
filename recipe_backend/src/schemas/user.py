from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User email")
    full_name: str | None = Field(default=None, description="Full name")
    is_active: bool | None = Field(default=True, description="Whether the user is active")


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="Password for the new user")
    full_name: str | None = Field(default=None, description="Full name")


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, description="Full name")
    password: str | None = Field(default=None, description="New password")


class UserPublic(BaseModel):
    id: int = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email")
    full_name: str | None = Field(default=None, description="Full name")
    is_active: bool = Field(..., description="Whether the user is active")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")

    class Config:
        from_attributes = True
