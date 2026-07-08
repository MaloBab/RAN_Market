from __future__ import annotations

import pytest

pytestmark = pytest.mark.asyncio


async def test_login_success_returns_access_token_and_sets_refresh_cookie(client, commercial_user):
    response = await client.post(
        "/auth/login", json={"email": "commercial@fanuc-ran.example", "password": "Commercial#2026"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["accessToken"]
    assert body["user"]["role"] == "commercial"
    assert "ran_refresh_token" in response.cookies


async def test_login_wrong_password_rejected(client, commercial_user):
    response = await client.post(
        "/auth/login", json={"email": "commercial@fanuc-ran.example", "password": "wrong-password"}
    )
    assert response.status_code == 401


async def test_login_unknown_email_gives_generic_error(client):
    response = await client.post(
        "/auth/login", json={"email": "nobody@fanuc-ran.example", "password": "whatever12345"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiants incorrects."


async def test_account_locks_after_repeated_failed_attempts(client, commercial_user):
    for _ in range(5):
        await client.post(
            "/auth/login", json={"email": "commercial@fanuc-ran.example", "password": "wrong"}
        )
    response = await client.post(
        "/auth/login", json={"email": "commercial@fanuc-ran.example", "password": "Commercial#2026"}
    )
    assert response.status_code == 401
    assert "verrouillé" in response.json()["detail"]


async def test_me_requires_authentication(client):
    response = await client.get("/auth/me")
    assert response.status_code == 401


async def test_me_with_valid_token(client, commercial_token):
    response = await client.get("/auth/me", headers={"Authorization": f"Bearer {commercial_token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "commercial@fanuc-ran.example"


async def test_refresh_rotates_token_and_old_one_becomes_invalid(client, commercial_user):
    login_resp = await client.post(
        "/auth/login", json={"email": "commercial@fanuc-ran.example", "password": "Commercial#2026"}
    )
    old_cookie = login_resp.cookies.get("ran_refresh_token")

    refresh_resp = await client.post("/auth/refresh")
    assert refresh_resp.status_code == 200
    new_cookie = refresh_resp.cookies.get("ran_refresh_token")
    assert new_cookie != old_cookie

    # Rejouer l'ancien cookie doit échouer (rotation effective).
    client.cookies.set("ran_refresh_token", old_cookie)
    replay_resp = await client.post("/auth/refresh")
    assert replay_resp.status_code == 401


async def test_logout_revokes_refresh_token(client, commercial_user):
    await client.post(
        "/auth/login", json={"email": "commercial@fanuc-ran.example", "password": "Commercial#2026"}
    )
    logout_resp = await client.post("/auth/logout")
    assert logout_resp.status_code == 204

    refresh_resp = await client.post("/auth/refresh")
    assert refresh_resp.status_code == 401


async def test_forbidden_error_message_never_leaks_stack_trace(client):
    response = await client.get("/robots/backoffice/all")
    assert response.status_code == 401
    assert "Traceback" not in response.text
