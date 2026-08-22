"""HTTP routes for the posts domain."""

from __future__ import annotations

from fastapi import APIRouter, status

from src.database import DbSession
from src.pagination import Page, PaginationDep
from src.posts import service
from src.posts.dependencies import ValidPost
from src.posts.models import Post
from src.posts.schemas import PostCreate, PostRead, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=Page[PostRead])
async def list_posts(db: DbSession, pagination: PaginationDep) -> Page[PostRead]:
    """Return a paginated list of posts."""
    items, total = await service.list_posts(db, pagination)
    return Page[PostRead](
        items=[PostRead.model_validate(item) for item in items],
        total=total,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(data: PostCreate, db: DbSession) -> Post:
    """Create a new post."""
    return await service.create_post(db, data)


@router.get("/{post_id}", response_model=PostRead)
async def get_post(post: ValidPost) -> Post:
    """Return a single post."""
    return post


@router.patch("/{post_id}", response_model=PostRead)
async def update_post(post: ValidPost, data: PostUpdate, db: DbSession) -> Post:
    """Update an existing post."""
    return await service.update_post(db, post, data)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post: ValidPost, db: DbSession) -> None:
    """Delete a post."""
    await service.delete_post(db, post)
