"""Utility helpers for the AWS external-service client."""

from __future__ import annotations

import re
from datetime import UTC, datetime

_SAFE_KEY = re.compile(r"[^a-zA-Z0-9._/-]+")


def build_object_key(prefix: str, filename: str) -> str:
    """Build a sanitized, timestamped S3 object key."""
    stamp = datetime.now(UTC).strftime("%Y/%m/%d")
    safe_prefix = _SAFE_KEY.sub("-", prefix).strip("-/")
    safe_name = _SAFE_KEY.sub("-", filename).strip("-")
    return f"{safe_prefix}/{stamp}/{safe_name}"
