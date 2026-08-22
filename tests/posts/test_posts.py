"""Tests for the posts domain."""

from __future__ import annotations

from httpx import AsyncClient


async def test_post_crud_flow(client: AsyncClient) -> None:
    created = await client.post(
        "/posts",
        json={"title": "Hello World", "body": "First post", "is_published": True},
    )
    assert created.status_code == 201
    post = created.json()
    assert post["slug"] == "hello-world"
    post_id = post["id"]

    listed = await client.get("/posts")
    assert listed.status_code == 200
    page = listed.json()
    assert page["total"] == 1
    assert page["items"][0]["id"] == post_id

    fetched = await client.get(f"/posts/{post_id}")
    assert fetched.status_code == 200

    updated = await client.patch(f"/posts/{post_id}", json={"title": "Updated Title"})
    assert updated.status_code == 200
    assert updated.json()["slug"] == "updated-title"

    deleted = await client.delete(f"/posts/{post_id}")
    assert deleted.status_code == 204
    assert (await client.get(f"/posts/{post_id}")).status_code == 404


async def test_get_missing_post_returns_404(client: AsyncClient) -> None:
    assert (await client.get("/posts/999")).status_code == 404
