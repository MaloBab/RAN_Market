from __future__ import annotations

from datetime import datetime

from pydantic import EmailStr, Field #type: ignore

from src.shared.enums import NiveauRenovation
from src.shared.schemas import CamelModel


class DevisRequestCreate(CamelModel):
    """POST /devis — aligné sur `DevisRequest` (frontend), endpoint public (formulaire client)."""

    prenom: str = Field(..., min_length=1, max_length=100)
    nom: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    telephone: str = Field(..., min_length=5, max_length=30)
    pays: str = Field(..., min_length=1, max_length=100)
    societe: str | None = Field(None, max_length=150)
    fonction: str | None = Field(None, max_length=150)
    robot_id: str | None = Field(None, max_length=50)
    prestations_souhaitees: list[NiveauRenovation] = Field(default_factory=list)
    demande_speciale: str | None = Field(None, max_length=2000)


class DevisSubmissionResult(CamelModel):
    """Aligné sur `DevisSubmissionResult` (frontend)."""

    reference: str
    commercial_assigne: str
    envoye_le: datetime


class DevisRequestSummary(CamelModel):
    """Vue back-office (liste des demandes reçues) — commercial/responsable_ran uniquement."""

    id: str
    reference: str
    prenom: str
    nom: str
    email: EmailStr
    telephone: str
    pays: str
    societe: str | None
    fonction: str | None
    robot_id: str | None
    prestations_souhaitees: list[NiveauRenovation]
    demande_speciale: str | None
    commercial_assigne: str
    envoye_le: datetime
