from __future__ import annotations

from pydantic import Field #type: ignore

from src.shared.enums import NiveauRenovation, RobotType
from src.shared.schemas import CamelModel


class ComingSoonResponse(CamelModel):
    id: str
    modele: str
    type: RobotType
    disponibilite_estimee: str
    niveau_renovation_prevu: NiveauRenovation


class ComingSoonCreate(CamelModel):
    id: str = Field(..., min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_-]+$")
    modele: str = Field(..., min_length=1, max_length=150)
    type: RobotType
    disponibilite_estimee: str = Field(..., min_length=1, max_length=30)
    niveau_renovation_prevu: NiveauRenovation


class ComingSoonUpdate(CamelModel):
    modele: str | None = Field(None, min_length=1, max_length=150)
    type: RobotType | None = None
    disponibilite_estimee: str | None = Field(None, min_length=1, max_length=30)
    niveau_renovation_prevu: NiveauRenovation | None = None
