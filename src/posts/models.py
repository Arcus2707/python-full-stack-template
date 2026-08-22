"""ORM models for the posts domain."""

from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base, TimestampMixin
from src.posts.constants import MAX_TITLE_LENGTH


class Post(Base, TimestampMixin):
    """A blog-style post."""

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(MAX_TITLE_LENGTH), index=True)
    slug: Mapped[str] = mapped_column(String(MAX_TITLE_LENGTH), unique=True, index=True)
    body: Mapped[str | None] = mapped_column(Text, default=None)
    is_published: Mapped[bool] = mapped_column(default=False)
