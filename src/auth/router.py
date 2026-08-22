"""HTTP routes for the auth domain."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth import service
from src.auth.dependencies import CurrentUser
from src.auth.models import User
from src.auth.schemas import Token, UserCreate, UserRead
from src.auth.utils import create_access_token
from src.database import DbSession

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: DbSession) -> User:
    """Register a new user."""
    return await service.create_user(db, data)


@router.post("/token", response_model=Token)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DbSession,
) -> Token:
    """Exchange credentials for an access token."""
    user = await service.authenticate(db, form.username, form.password)
    return Token(access_token=create_access_token(str(user.id)))


@router.get("/me", response_model=UserRead)
async def read_me(user: CurrentUser) -> User:
    """Return the currently authenticated user."""
    return user
