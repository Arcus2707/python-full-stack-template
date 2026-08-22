"""Tests for the auth domain."""

from __future__ import annotations

from httpx import AsyncClient


async def test_register_login_and_me(client: AsyncClient) -> None:
    register = await client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "supersecret"},
    )
    assert register.status_code == 201
    assert register.json()["email"] == "user@example.com"

    token_resp = await client.post(
        "/auth/token",
        data={"username": "user@example.com", "password": "supersecret"},
    )
    assert token_resp.status_code == 200
    token = token_resp.json()["access_token"]

    me = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "user@example.com"


async def test_duplicate_email_rejected(client: AsyncClient) -> None:
    payload = {"email": "dupe@example.com", "password": "supersecret"}
    assert (await client.post("/auth/register", json=payload)).status_code == 201
    second = await client.post("/auth/register", json=payload)
    assert second.status_code == 400


async def test_invalid_credentials(client: AsyncClient) -> None:
    resp = await client.post(
        "/auth/token",
        data={"username": "nobody@example.com", "password": "wrongpass"},
    )
    assert resp.status_code == 401


async def test_me_requires_auth(client: AsyncClient) -> None:
    assert (await client.get("/auth/me")).status_code == 401
