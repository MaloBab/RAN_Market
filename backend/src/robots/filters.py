from __future__ import annotations

from dataclasses import dataclass, field

from src.shared.enums import BaieType, RobotType


@dataclass
class NumericRange:
    min: float | None = None
    max: float | None = None


@dataclass
class CatalogueFilters:
    """
    Filtres cumulables du catalogue (CDC §3.1) — pendant serveur de
    `CatalogueFilters` (frontend/src/types/filters.types.ts). Toutes les
    bornes sont inclusives ; `None` = filtre inactif.
    """

    recherche: str = ""
    types: list[RobotType] = field(default_factory=list)
    payload_kg: NumericRange | None = None
    rayon_action_m: NumericRange | None = None
    axes: list[int] = field(default_factory=list)
    type_baie: BaieType | None = None
    annee_mise_en_service: NumericRange | None = None
    heures_utilisation: NumericRange | None = None
