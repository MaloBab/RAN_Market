"""
Base Pydantic partagée par tous les domaines.

Le frontend Vue existant (`frontend/src/types/*.ts`) consomme des clés JSON
en camelCase (`anneeMiseEnService`, `payloadKg`, `prixCatalogueEUR`...).
Plutôt que de renommer manuellement chaque champ, on génère les alias
automatiquement à partir des noms de champs Python en snake_case — ce qui
garde le code Python idiomatique tout en produisant un contrat JSON
strictement identique à celui déjà attendu par `api.contracts.ts`, sans
aucune modification du frontend.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


def to_camel(snake_str: str) -> str:
    first, *rest = snake_str.split("_")
    return first + "".join(word.capitalize() for word in rest)


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
