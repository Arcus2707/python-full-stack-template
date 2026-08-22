"""Reusable pagination primitives shared across API endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel

DEFAULT_LIMIT = 50
MAX_LIMIT = 100


class PaginationParams(BaseModel):
    """Validated ``limit``/``offset`` query parameters."""

    limit: int = DEFAULT_LIMIT
    offset: int = 0


class Page[M](BaseModel):
    """A paginated response envelope."""

    items: list[M]
    total: int
    limit: int
    offset: int


async def pagination_params(
    limit: Annotated[int, Query(ge=1, le=MAX_LIMIT)] = DEFAULT_LIMIT,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> PaginationParams:
    """FastAPI dependency producing validated pagination parameters."""
    return PaginationParams(limit=limit, offset=offset)


PaginationDep = Annotated[PaginationParams, Depends(pagination_params)]
