from __future__ import annotations

from io import BytesIO

import pytest
from openpyxl import Workbook

pytestmark = pytest.mark.asyncio

COLUMNS = [
    "ID_Robot", "Modèle", "Type", "Payload_kg", "Rayon_mm", "Axes", "Type_baie",
    "Annee_service", "Heures_utilisation", "Quantite_stock", "Prix_catalogue_EUR",
    "Remise_pct", "Prestations_dispo", "Protection_IP", "Description_courte",
]


def _build_workbook(rows: list[list]) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.append(COLUMNS)
    for row in rows:
        ws.append(row)
    buffer = BytesIO()
    wb.save(buffer)
    return buffer.getvalue()


async def test_import_creates_draft_robots(client, responsable_token):
    content = _build_workbook(
        [
            [
                "FANUC-2024-IMP1", "ARC Mate 100iD", "Soudure arc", 12, 1441, 6, "R-30iB Plus",
                2018, 14500, 3, 28000, 10, "Standard;Premium", "IP54", "Robot importé",
            ]
        ]
    )
    headers = {"Authorization": f"Bearer {responsable_token}"}
    files = {"file": ("import.xlsx", content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    response = await client.post("/imports/robots", files=files, headers=headers)
    assert response.status_code == 200, response.text
    report = response.json()
    assert report["accepte"] == 1
    assert report["erreurs"] == 0
    assert report["details"][0]["statut"] == "accepte"

    robot_resp = await client.get(f"/robots/backoffice/all", headers=headers)
    robots = robot_resp.json()
    imported = next(r for r in robots if r["id"] == "FANUC-2024-IMP1")
    assert imported["statut"] == "Brouillon"


async def test_import_detects_duplicate_rows(client, responsable_token):
    content = _build_workbook(
        [
            ["FANUC-2024-DUP1", "Modèle", "Articulé", 10, 1000, 6, "R-30iB", 2020, 1000, 1, 10000, 0, "", "IP54", "x"],
            ["FANUC-2024-DUP1", "Modèle", "Articulé", 10, 1000, 6, "R-30iB", 2020, 1000, 1, 10000, 0, "", "IP54", "x"],
        ]
    )
    headers = {"Authorization": f"Bearer {responsable_token}"}
    files = {"file": ("import.xlsx", content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    response = await client.post("/imports/robots", files=files, headers=headers)
    report = response.json()
    assert report["accepte"] == 1
    assert report["doublons"] == 1


async def test_import_rejects_non_xlsx_file(client, responsable_token):
    headers = {"Authorization": f"Bearer {responsable_token}"}
    files = {"file": ("notes.txt", b"hello world", "text/plain")}
    response = await client.post("/imports/robots", files=files, headers=headers)
    assert response.status_code == 422


async def test_import_requires_responsable_role(client, commercial_token):
    content = _build_workbook([])
    headers = {"Authorization": f"Bearer {commercial_token}"}
    files = {"file": ("import.xlsx", content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    response = await client.post("/imports/robots", files=files, headers=headers)
    assert response.status_code == 403
