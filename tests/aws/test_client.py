"""Tests for the AWS external-service client."""

from __future__ import annotations

from src.aws.client import AWSClient
from src.aws.schemas import UploadRequest
from src.aws.utils import build_object_key


async def test_upload_builds_key_and_url() -> None:
    client = AWSClient()
    result = await client.upload(UploadRequest(filename="report.pdf", prefix="docs"))
    assert result.bucket == client.config.bucket
    assert result.key.startswith("docs/")
    assert result.key.endswith("report.pdf")
    assert result.url.endswith(result.key)


async def test_presigned_url_has_expiry() -> None:
    client = AWSClient()
    url = await client.generate_presigned_url("docs/report.pdf", ttl=120)
    assert "X-Amz-Expires=120" in url


def test_build_object_key_sanitizes() -> None:
    key = build_object_key("un safe/prefix", "my file!.png")
    assert " " not in key
    assert "!" not in key
