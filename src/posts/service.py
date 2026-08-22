"""Business logic for the posts domain."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.pagination import PaginationParams
from src.posts.models import Post
from src.posts.schemas import PostCreate, PostUpdate
from src.posts.utils import slugify


async def list_posts(db: AsyncSession, pagination: PaginationParams) -> tuple[list[Post], int]:
    """Return a page of posts and the total count."""
    total = await db.scalar(select(func.count()).select_from(Post)) or 0
    result = await db.execute(
        select(Post).order_by(Post.id).limit(pagination.limit).offset(pagination.offset)
    )
    return list(result.scalars().all()), total


async def get_post(db: AsyncSession, post_id: int) -> Post | None:
    """Return a post by id, if it exists."""
    return await db.get(Post, post_id)


async def create_post(db: AsyncSession, data: PostCreate) -> Post:
    """Create a new post."""
    post = Post(**data.model_dump(), slug=slugify(data.title))
    db.add(post)
    await db.flush()
    await db.refresh(post)
    return post


async def update_post(db: AsyncSession, post: Post, data: PostUpdate) -> Post:
    """Apply a partial update to an existing post."""
    values = data.model_dump(exclude_unset=True)
    if "title" in values:
        post.slug = slugify(values["title"])
    for field, value in values.items():
        setattr(post, field, value)
    await db.flush()
    await db.refresh(post)
    return post


async def delete_post(db: AsyncSession, post: Post) -> None:
    """Delete a post."""
    await db.delete(post)
    await db.flush()
