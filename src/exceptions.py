"""Global exception hierarchy and shared error responses.

Domains raise these (or their own subclasses in ``<domain>/exceptions.py``) so
error handling is consistent across the application.
"""

from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    """Base HTTP exception with class-level status code and detail."""

    STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL: str = "Server error"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class BadRequest(DetailedHTTPException):
    """400 Bad Request."""

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad request"


class NotAuthenticated(DetailedHTTPException):
    """401 Unauthorized."""

    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "User not authenticated"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})


class PermissionDenied(DetailedHTTPException):
    """403 Forbidden."""

    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Permission denied"


class NotFound(DetailedHTTPException):
    """404 Not Found."""

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Resource not found"


class Conflict(DetailedHTTPException):
    """409 Conflict."""

    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "Resource already exists"
