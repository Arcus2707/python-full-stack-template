# Caching

Caching uses [aiocache](https://aiocache.aio-libs.org/) backed by Redis,
configured in [`src/cache.py`](../../src/cache.py).

## Configuration

`configure_cache()` registers a `default` cache from settings during
application startup (`lifespan`). The Redis endpoint and default TTL come from
`APP_REDIS_URL` and `APP_CACHE_TTL`.

## Usage

Inject the cache in FastAPI routes:

```python
from src.cache import CacheDep

@router.get("/posts/{post_id}/cached")
async def cached(post_id: int, cache: CacheDep) -> dict[str, int]:
    key = f"post:{post_id}"
    if (hit := await cache.get(key)) is not None:
        return hit
    value = {"id": post_id}
    await cache.set(key, value, ttl=60)
    return value
```

## Decorator usage

aiocache provides decorators for transparent memoization:

```python
from aiocache import cached
from src.config import get_settings

@cached(ttl=get_settings().cache_ttl, key_builder=lambda f, *a, **kw: f"sum:{a}")
async def expensive(a: int, b: int) -> int:
    ...
```

## TTL strategies

Use different TTLs per access pattern:

- Short (30–60s) for frequently changing data
- Medium (5–15m, the default `APP_CACHE_TTL`) for typical reads
- Long (hours) for rarely changing reference data

## Cache warming

Pre-populate hot keys on startup inside the `lifespan` hook so the first
requests hit a warm cache:

```python
from src.cache import get_cache

async def warm_cache() -> None:
    cache = get_cache()
    await cache.set("config:featured", await load_featured(), ttl=3600)
```
