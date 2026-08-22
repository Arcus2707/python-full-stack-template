"""Password hashing and JWT helpers for the auth domain."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from src.auth.config import get_auth_config
from src.auth.constants import SCRYPT_DKLEN, SCRYPT_N, SCRYPT_P, SCRYPT_R


def hash_password(password: str) -> str:
    """Hash a password with a random salt using scrypt (stdlib)."""
    salt = secrets.token_bytes(16)
    derived = hashlib.scrypt(
        password.encode(),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=SCRYPT_DKLEN,
    )
    return f"{salt.hex()}${derived.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    """Verify a plaintext password against a stored scrypt hash."""
    try:
        salt_hex, hash_hex = hashed.split("$", 1)
    except ValueError:
        return False
    derived = hashlib.scrypt(
        password.encode(),
        salt=bytes.fromhex(salt_hex),
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=SCRYPT_DKLEN,
    )
    return hmac.compare_digest(derived.hex(), hash_hex)


def create_access_token(subject: str) -> str:
    """Create a signed JWT access token for ``subject``."""
    config = get_auth_config()
    now = datetime.now(UTC)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=config.access_token_expire_minutes),
    }
    return jwt.encode(payload, config.secret_key.get_secret_value(), algorithm=config.algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT access token, returning its claims."""
    config = get_auth_config()
    return jwt.decode(
        token,
        config.secret_key.get_secret_value(),
        algorithms=[config.algorithm],
    )
