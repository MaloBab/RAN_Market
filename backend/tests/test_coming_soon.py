from __future__ import annotations

import pytest

pytestmark = pytest.mark.asyncio


async def test_anonymous_cannot_see_coming_soon(client):
    response = await client.get("/coming-soon")
    assert response.status_code == 401


async def test_commercial_can_list_coming_soon(client, commercial_token, responsable_token):
    headers_ran = {"Authorization": f"Bearer {responsable_token}"}
    await client.post(
        "/coming-soon",
        json={
            "id": "CS-001", "modele": "R-2000iC", "type": "Articulé",
            "disponibiliteEstimee": "T1 2027", "niveauRenovationPrevu": "Premium",
        },
        headers=headers_ran,
    )
    headers_com = {"Authorization": f"Bearer {commercial_token}"}
    response = await client.get("/coming-soon", headers=headers_com)
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_commercial_cannot_create_coming_soon_entry(client, commercial_token):
    headers = {"Authorization": f"Bearer {commercial_token}"}
    response = await client.post(
        "/coming-soon",
        json={
            "id": "CS-002", "modele": "R-2000iC", "type": "Articulé",
            "disponibiliteEstimee": "T1 2027", "niveauRenovationPrevu": "Premium",
        },
        headers=headers,
    )
    assert response.status_code == 403
