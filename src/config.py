"""Global, type-safe application configuration backed by Pydantic Settings.

Settings are loaded from (in priority order): environment variables, a local
``.env`` file, and the defaults declared here. Every variable is validated at
startup so misconfiguration fails fast with a clear error message.

Domain-specific configuration lives in each package's ``config.py`` (for
example ``src/auth/config.py``).
"""

from __future__ import annotations

from enum import StrEnum
from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """Deployment environments the application can run in."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class Settings(BaseSettings):
    """Central application settings.

    Extend this class by adding new typed fields; they are automatically
    populated from environment variables prefixed with ``APP_``.
    """

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- Core ---------------------------------------------------------------
    env: Environment = Environment.DEVELOPMENT
    debug: bool = False
    name: str = "Python Full-Stack Template"
    secret_key: SecretStr = SecretStr("change-me-in-production")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # --- Server -------------------------------------------------------------
    host: str = "0.0.0.0"  # noqa: S104 - configurable bind address
    port: int = Field(default=8000, ge=1, le=65535)

    # --- Database -----------------------------------------------------------
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/app"
    database_echo: bool = False

    # --- Cache / Redis ------------------------------------------------------
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl: int = Field(default=300, ge=0)

    # --- Celery -------------------------------------------------------------
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    @property
    def is_production(self) -> bool:
        """Return ``True`` when running in the production environment."""
        return self.env is Environment.PRODUCTION

    @field_validator("secret_key")
    @classmethod
    def _reject_empty_secret(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value():
            msg = "secret_key must not be empty"
            raise ValueError(msg)
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance.

    Cached so the ``.env`` file and environment are parsed only once per
    process. Call ``get_settings.cache_clear()`` in tests to reload.
    """
    return Settings()
