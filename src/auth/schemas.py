"""Pydantic schemas for the auth domain."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    """Shared user fields."""

    email: str


class UserCreate(UserBase):
    """Payload to register a new user."""

    password: str = Field(min_length=8, max_length=128)


class UserRead(UserBase):
    """Public user representation."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool


class Token(BaseModel):
    """OAuth2 bearer token response."""

    access_token: str
    token_type: str = "bearer"  # noqa: S105 - OAuth2 token type label, not a secret


class TokenPayload(BaseModel):
    """Decoded JWT claims."""

    sub: str
