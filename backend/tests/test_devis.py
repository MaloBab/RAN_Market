from __future__ import annotations

import pytest

pytestmark = pytest.mark.asyncio


async def test_public_can_submit_devis_request(client, commercial_user):
    response = await client.post(
        "/devis",
        json={
            "prenom": "Alice",
            "nom": "Martin",
            "email": "alice.martin@example.com",
            "telephone": "+33612345678",
            "pays": "France",
            "prestationsSouhaitees": ["Standard"],
        },
    )
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["reference"].startswith("DEV-")
    assert body["commercialAssigne"] == "Camille Berthier"


async def test_devis_list_requires_authentication(client):
    response = await client.get("/devis")
    assert response.status_code == 401


async def test_devis_list_visible_to_commercial(client, commercial_user, commercial_token):
    await client.post(
        "/devis",
        json={
            "prenom": "Bob", "nom": "Dupont", "email": "bob@example.com",
            "telephone": "0600000000", "pays": "France", "prestationsSouhaitees": [],
        },
    )
    headers = {"Authorization": f"Bearer {commercial_token}"}
    response = await client.get("/devis", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_devis_with_no_commercial_available_fails_gracefully(client):
    response = await client.post(
        "/devis",
        json={
            "prenom": "Nobody", "nom": "Here", "email": "nobody@example.com",
            "telephone": "0600000000", "pays": "France", "prestationsSouhaitees": [],
        },
    )
    assert response.status_code == 400
