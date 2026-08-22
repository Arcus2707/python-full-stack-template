"""Constants and error messages for the auth domain."""

from __future__ import annotations


class ErrorCode:
    """Human-readable error messages for auth failures."""

    EMAIL_TAKEN = "Email is already registered."
    INVALID_CREDENTIALS = "Incorrect email or password."
    INVALID_TOKEN = "Could not validate credentials."  # noqa: S105 - error message, not a secret


# scrypt cost parameters (RFC 7914). Tune for your hardware.
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1
SCRYPT_DKLEN = 32
