"""Shared pytest fixtures."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator

import pytest

# Configure a fully in-memory, isolated environment before app imports.
os.environ.update(
    {
        "APP_ENV": "testing",
        "APP_DATABASE_URL": "sqlite+aiosqlite:///:memory:",
        "APP_REDIS_URL": "redis://localhost:6379/0",
        "APP_SECRET_KEY": "test-secret-key-for-tests-0123456789abcdef",
        "APP_AUTH_SECRET_KEY": "test-secret-key-for-tests-0123456789abcdef",
    }
)

from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from src.auth.config import get_auth_config
from src.auth.models import User  # noqa: F401 - register metadata
from src.aws.config import get_aws_config
from src.config import get_settings
from src.database import get_db
from src.main import create_app
from src.models import Base
from src.posts.models import Post  # noqa: F401 - register metadata


@pytest.fixture(autouse=True)
def _reset_caches() -> None:
    """Ensure each test sees freshly parsed configuration."""
    get_settings.cache_clear()
    get_auth_config.cache_clear()
    get_aws_config.cache_clear()


@pytest.fixture
async def engine() -> AsyncIterator[AsyncEngine]:
    """Provide a shared in-memory SQLite engine with tables created."""
    eng = create_async_engine(
        "sqlite+aiosqlite://",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    await eng.dispose()


@pytest.fixture
def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Return a session factory bound to the test engine."""
    return async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture
async def db_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    """Provide an isolated database session for direct service tests."""
    async with session_factory() as session:
        yield session


@pytest.fixture
async def client(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncClient]:
    """Provide an HTTP client bound to the ASGI app using the test database."""
    app = create_app()

    async def override_get_db() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac
    app.dependency_overrides.clear()
