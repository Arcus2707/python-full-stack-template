"""Business logic for the auth domain."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import utils
from src.auth.exceptions import EmailAlreadyRegistered, InvalidCredentials
from src.auth.models import User
from src.auth.schemas import UserCreate


async def get_by_email(db: AsyncSession, email: str) -> User | None:
    """Return the user with the given email, if any."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Return the user with the given id, if any."""
    return await db.get(User, user_id)


async def create_user(db: AsyncSession, data: UserCreate) -> User:
    """Create a new user, rejecting duplicate emails."""
    if await get_by_email(db, data.email) is not None:
        raise EmailAlreadyRegistered
    user = User(email=data.email, hashed_password=utils.hash_password(data.password))
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def authenticate(db: AsyncSession, email: str, password: str) -> User:
    """Return the user if the credentials are valid, else raise."""
    user = await get_by_email(db, email)
    if user is None or not utils.verify_password(password, user.hashed_password):
        raise InvalidCredentials
    return user
