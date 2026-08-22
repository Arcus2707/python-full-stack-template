"""Auth-specific exceptions built on the global exception hierarchy."""

from __future__ import annotations

from src.auth.constants import ErrorCode
from src.exceptions import BadRequest, NotAuthenticated


class EmailAlreadyRegistered(BadRequest):
    """Raised when registering an email that already exists."""

    DETAIL = ErrorCode.EMAIL_TAKEN


class InvalidCredentials(NotAuthenticated):
    """Raised when authentication fails."""

    DETAIL = ErrorCode.INVALID_CREDENTIALS


class InvalidToken(NotAuthenticated):
    """Raised when a bearer token is missing, expired or malformed."""

    DETAIL = ErrorCode.INVALID_TOKEN
