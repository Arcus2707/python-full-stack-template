"""Pydantic schemas for the posts domain."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from src.posts.constants import MAX_TITLE_LENGTH


class PostBase(BaseModel):
    """Shared post fields."""

    title: str = Field(min_length=1, max_length=MAX_TITLE_LENGTH)
    body: str | None = None
    is_published: bool = False


class PostCreate(PostBase):
    """Payload to create a post."""


class PostUpdate(BaseModel):
    """Payload to partially update a post."""

    title: str | None = Field(default=None, min_length=1, max_length=MAX_TITLE_LENGTH)
    body: str | None = None
    is_published: bool | None = None


class PostRead(PostBase):
    """Serialized post representation."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
