"""Application-level tests (health endpoint and settings)."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from src.config import Environment, Settings


async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["environment"] == "testing"
    assert "version" in body


async def test_index_renders_html(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.port == 8000
    assert isinstance(settings.env, Environment)


def test_settings_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_PORT", "9000")
    monkeypatch.setenv("APP_ENV", "production")
    settings = Settings()
    assert settings.port == 9000
    assert settings.is_production is True


def test_settings_invalid_port(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_PORT", "70000")
    with pytest.raises(ValueError, match="port"):
        Settings()
