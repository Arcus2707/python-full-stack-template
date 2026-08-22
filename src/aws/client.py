"""Client model for communicating with the external AWS service.

This is an illustrative, dependency-free stub that demonstrates the pattern for
wrapping an external service: configuration is injected, calls are async, and
failures raise a domain exception. Replace the method bodies with real calls
(e.g. via ``aioboto3``) for production use.
"""

from __future__ import annotations

from src.aws.config import AWSConfig, get_aws_config
from src.aws.constants import PRESIGNED_URL_TTL
from src.aws.schemas import UploadRequest, UploadResult
from src.aws.utils import build_object_key


class AWSClient:
    """Thin async wrapper around an external object-storage service."""

    def __init__(self, config: AWSConfig | None = None) -> None:
        self._config = config or get_aws_config()

    @property
    def config(self) -> AWSConfig:
        """Return the client configuration."""
        return self._config

    def _object_url(self, key: str) -> str:
        base = (
            self._config.endpoint_url
            or f"https://{self._config.bucket}.s3.{self._config.region}.amazonaws.com"
        )
        return f"{base.rstrip('/')}/{key}"

    async def upload(self, request: UploadRequest) -> UploadResult:
        """Upload an object and return its storage location."""
        key = build_object_key(request.prefix, request.filename)
        # Real implementation would stream bytes to the bucket here.
        return UploadResult(bucket=self._config.bucket, key=key, url=self._object_url(key))

    async def generate_presigned_url(self, key: str, ttl: int = PRESIGNED_URL_TTL) -> str:
        """Return a time-limited URL for the given object key."""
        return f"{self._object_url(key)}?X-Amz-Expires={ttl}"


def get_aws_client() -> AWSClient:
    """Return a configured AWS client instance."""
    return AWSClient()
