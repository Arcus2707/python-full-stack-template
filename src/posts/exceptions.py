"""Exceptions for the posts domain."""

from __future__ import annotations

from src.exceptions import NotFound
from src.posts.constants import ErrorCode


class PostNotFound(NotFound):
    """Raised when a post does not exist."""

    DETAIL = ErrorCode.POST_NOT_FOUND
