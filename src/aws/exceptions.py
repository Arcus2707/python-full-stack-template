"""Exceptions for the AWS external-service client."""

from __future__ import annotations

from fastapi import status

from src.exceptions import DetailedHTTPException


class AWSServiceError(DetailedHTTPException):
    """Raised when the external AWS service call fails."""

    STATUS_CODE = status.HTTP_502_BAD_GATEWAY
    DETAIL = "Upstream AWS service error"
