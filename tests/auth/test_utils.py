"""Tests for password hashing and JWT utilities."""

from __future__ import annotations

from src.auth import utils


def test_password_hash_roundtrip() -> None:
    hashed = utils.hash_password("supersecret")
    assert hashed != "supersecret"
    assert utils.verify_password("supersecret", hashed)
    assert not utils.verify_password("wrong", hashed)


def test_verify_rejects_malformed_hash() -> None:
    assert not utils.verify_password("secret", "not-a-valid-hash")


def test_access_token_roundtrip() -> None:
    token = utils.create_access_token("42")
    claims = utils.decode_access_token(token)
    assert claims["sub"] == "42"
