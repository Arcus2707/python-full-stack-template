"""Pydantic schemas for the AWS external-service client."""

from __future__ import annotations

from pydantic import BaseModel


class UploadRequest(BaseModel):
    """Request to upload an object."""

    filename: str
    content_type: str = "application/octet-stream"
    prefix: str = "uploads"


class UploadResult(BaseModel):
    """Result of an upload operation."""

    bucket: str
    key: str
    url: str
