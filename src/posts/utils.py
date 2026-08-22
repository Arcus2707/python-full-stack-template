"""Utility helpers for the posts domain."""

from __future__ import annotations

import re

_SLUG_STRIP = re.compile(r"[^a-z0-9]+")


def slugify(title: str) -> str:
    """Convert a title into a URL-friendly slug."""
    return _SLUG_STRIP.sub("-", title.lower()).strip("-")
