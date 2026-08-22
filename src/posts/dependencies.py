"""FastAPI dependencies for the posts domain."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from src.database import DbSession
from src.posts import service
from src.posts.exceptions import PostNotFound
from src.posts.models import Post


async def valid_post_id(post_id: int, db: DbSession) -> Post:
    """Resolve and return an existing post or raise ``PostNotFound``."""
    post = await service.get_post(db, post_id)
    if post is None:
        raise PostNotFound
    return post


ValidPost = Annotated[Post, Depends(valid_post_id)]
