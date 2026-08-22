"""Local configuration for the auth domain."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    """JWT and password settings, loaded from ``APP_AUTH_*`` variables."""

    model_config = SettingsConfigDict(
        env_prefix="APP_AUTH_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    secret_key: SecretStr = SecretStr("change-me-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=60, ge=1)


@lru_cache(maxsize=1)
def get_auth_config() -> AuthConfig:
    """Return the cached auth configuration."""
    return AuthConfig()
