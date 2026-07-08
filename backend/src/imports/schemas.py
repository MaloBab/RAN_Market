from __future__ import annotations

from src.shared.enums import ImportRowStatus
from src.shared.schemas import CamelModel


class ImportRowResultSchema(CamelModel):
    ligne: int
    id_robot: str
    statut: ImportRowStatus
    message: str | None = None


class ImportReport(CamelModel):
    """Aligné sur `ImportReport` (frontend/src/types/import.types.ts)."""

    total_lignes: int
    accepte: int
    erreurs: int
    doublons: int
    details: list[ImportRowResultSchema]
