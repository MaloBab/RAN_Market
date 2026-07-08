from __future__ import annotations

import pytest

pytestmark = pytest.mark.asyncio


def _valid_robot_payload(robot_id: str = "FANUC-2024-999") -> dict:
    return {
        "id": robot_id,
        "modele": "ARC Mate 100iD",
        "type": "Soudure arc",
        "categorie": "Soudure arc",
        "anneeMiseEnService": 2020,
        "heuresUtilisation": 5000,
        "descriptionCourte": "Robot de test",
        "caracteristiques": {
            "payloadKg": 12,
            "rayonActionMm": 1441,
            "axes": 6,
            "typeBaie": "R-30iB Plus",
            "protectionIp": "IP54",
            "montage": "Sol",
        },
        "prestationsDisponibles": [{"niveau": "Standard", "garantieMois": 12}],
        "media": {"photosAvant": [], "galerieAvantApres": []},
        "documentation": {},
        "prixCatalogueEUR": 28000,
        "remisePct": 10,
        "quantiteStock": 2,
        "nombreOffresEnCours": 0,
    }


async def test_client_view_never_contains_commercial_data(client, responsable_token):
    headers = {"Authorization": f"Bearer {responsable_token}"}
    create_resp = await client.post("/robots", json=_valid_robot_payload(), headers=headers)
    assert create_resp.status_code == 201, create_resp.text
    robot_id = create_resp.json()["id"]

    await client.patch(f"/robots/{robot_id}", json={"statut": "Publié"}, headers=headers)

    anon_resp = await client.get(f"/robots/{robot_id}")
    assert anon_resp.status_code == 200
    body = anon_resp.json()
    assert "commercial" not in body
    assert "statut" not in body
    assert "prixFinalEUR" not in body


async def test_commercial_view_contains_pricing(client, responsable_token, commercial_token):
    headers_ran = {"Authorization": f"Bearer {responsable_token}"}
    create_resp = await client.post("/robots", json=_valid_robot_payload(), headers=headers_ran)
    robot_id = create_resp.json()["id"]
    await client.patch(f"/robots/{robot_id}", json={"statut": "Publié"}, headers=headers_ran)

    headers_com = {"Authorization": f"Bearer {commercial_token}"}
    resp = await client.get(f"/robots/{robot_id}", headers=headers_com)
    assert resp.status_code == 200
    body = resp.json()
    assert body["commercial"]["prixCatalogueEUR"] == 28000
    assert body["prixFinalEUR"] == 25200.0  # 28000 * (1 - 10%)


async def test_draft_robot_never_visible_via_public_catalogue(client, responsable_token):
    headers = {"Authorization": f"Bearer {responsable_token}"}
    create_resp = await client.post("/robots", json=_valid_robot_payload(), headers=headers)
    robot_id = create_resp.json()["id"]
    assert create_resp.json()["statut"] == "Brouillon"

    # Ni en vue anonyme, ni même en vue commerciale authentifiée : pas encore publié.
    anon_resp = await client.get(f"/robots/{robot_id}")
    assert anon_resp.status_code == 404


async def test_commercial_cannot_create_robot(client, commercial_token):
    headers = {"Authorization": f"Bearer {commercial_token}"}
    response = await client.post("/robots", json=_valid_robot_payload(), headers=headers)
    assert response.status_code == 403


async def test_anonymous_cannot_create_robot(client):
    response = await client.post("/robots", json=_valid_robot_payload())
    assert response.status_code == 401


async def test_duplicate_robot_id_rejected(client, responsable_token):
    headers = {"Authorization": f"Bearer {responsable_token}"}
    payload = _valid_robot_payload("FANUC-2024-DUP")
    first = await client.post("/robots", json=payload, headers=headers)
    assert first.status_code == 201
    second = await client.post("/robots", json=payload, headers=headers)
    assert second.status_code == 409


async def test_invalid_axes_count_rejected(client, responsable_token):
    headers = {"Authorization": f"Bearer {responsable_token}"}
    payload = _valid_robot_payload("FANUC-2024-BADAXES")
    payload["caracteristiques"]["axes"] = 3
    response = await client.post("/robots", json=payload, headers=headers)
    assert response.status_code == 422


async def test_compare_requires_commercial_role(client, responsable_token, commercial_token):
    headers_ran = {"Authorization": f"Bearer {responsable_token}"}
    for suffix in ("A", "B"):
        payload = _valid_robot_payload(f"FANUC-2024-CMP{suffix}")
        create_resp = await client.post("/robots", json=payload, headers=headers_ran)
        rid = create_resp.json()["id"]
        await client.patch(f"/robots/{rid}", json={"statut": "Publié"}, headers=headers_ran)

    anon_resp = await client.get("/robots/compare", params={"ids": ["FANUC-2024-CMPA", "FANUC-2024-CMPB"]})
    assert anon_resp.status_code == 401

    headers_com = {"Authorization": f"Bearer {commercial_token}"}
    com_resp = await client.get(
        "/robots/compare", params={"ids": ["FANUC-2024-CMPA", "FANUC-2024-CMPB"]}, headers=headers_com
    )
    assert com_resp.status_code == 200
    assert len(com_resp.json()) == 2
