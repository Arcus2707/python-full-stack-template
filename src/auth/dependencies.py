"""FastAPI dependencies for the auth domain."""

from __future__ import annotations

from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.auth import service
from src.auth.exceptions import InvalidToken
from src.auth.models import User
from src.auth.utils import decode_access_token
from src.database import DbSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DbSession,
) -> User:
    """Resolve the authenticated user from a bearer token."""
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError) as exc:
        raise InvalidToken from exc
    user = await service.get_by_id(db, user_id)
    if user is None:
        raise InvalidToken
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
