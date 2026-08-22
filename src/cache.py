"""aiocache integration providing a shared, Redis-backed cache."""

from __future__ import annotations

from typing import Annotated

from aiocache import Cache, caches
from fastapi import Depends

from src.config import Settings, get_settings


def configure_cache(settings: Settings | None = None) -> None:
    """Configure the global aiocache registry from application settings."""
    settings = settings or get_settings()
    caches.set_config(
        {
            "default": {
                "cache": "aiocache.RedisCache",
                "endpoint": settings.redis_url.split("//", 1)[-1].split(":")[0] or "localhost",
                "ttl": settings.cache_ttl,
                "serializer": {"class": "aiocache.serializers.JsonSerializer"},
            },
        }
    )


def get_cache() -> Cache:
    """Return the configured default cache instance."""
    return caches.get("default")


CacheDep = Annotated[Cache, Depends(get_cache)]

__all__ = ["Cache", "CacheDep", "configure_cache", "get_cache"]
