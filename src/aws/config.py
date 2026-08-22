"""Local configuration for the AWS external-service client."""

from __future__ import annotations

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.aws.constants import DEFAULT_REGION


class AWSConfig(BaseSettings):
    """AWS client settings, loaded from ``APP_AWS_*`` variables."""

    model_config = SettingsConfigDict(
        env_prefix="APP_AWS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    region: str = DEFAULT_REGION
    access_key_id: str = ""
    secret_access_key: SecretStr = SecretStr("")
    bucket: str = "example-bucket"
    endpoint_url: str | None = None


@lru_cache(maxsize=1)
def get_aws_config() -> AWSConfig:
    """Return the cached AWS configuration."""
    return AWSConfig()
