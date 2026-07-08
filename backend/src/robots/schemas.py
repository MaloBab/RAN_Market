from __future__ import annotations

from pydantic import Field, field_validator

from src.shared.enums import BaieType, NiveauRenovation, RobotStatut, RobotType
from src.shared.schemas import CamelModel

AXES_AUTORISES = {4, 5, 6, 7}


# ---------------------------------------------------------------------------
# Blocs communs (imbriqués) — alignés sur robot.types.ts
# ---------------------------------------------------------------------------

class CaracteristiquesSchema(CamelModel):
    payload_kg: float = Field(..., gt=0, le=2000)
    rayon_action_mm: int = Field(..., gt=0, le=10000)
    axes: int = Field(..., ge=4, le=7)
    type_baie: BaieType
    protection_ip: str = Field(..., min_length=1, max_length=30)
    montage: str = Field(..., min_length=1, max_length=100)

    @field_validator("axes")
    @classmethod
    def check_axes_autorises(cls, v: int) -> int:
        if v not in AXES_AUTORISES:
            raise ValueError("Le nombre d'axes doit être 4, 5, 6 ou 7.")
        return v


class DocumentationSchema(CamelModel):
    datasheet_url: str | None = Field(None, max_length=500)
    flyer_url: str | None = Field(None, max_length=500)
    brochure_url: str | None = Field(None, max_length=500)


class GalerieItemSchema(CamelModel):
    avant: str = Field(..., max_length=500)
    apres: str = Field(..., max_length=500)
    legende: str | None = Field(None, max_length=200)


class MediaSchema(CamelModel):
    photos_avant: list[str] = Field(default_factory=list)
    galerie_avant_apres: list[GalerieItemSchema] = Field(default_factory=list)
    video_url: str | None = Field(None, max_length=500)


class PrestationSchema(CamelModel):
    niveau: NiveauRenovation
    garantie_mois: int | None = Field(None, ge=0, le=60)


class VenteHistoriqueSchema(CamelModel):
    periode: str = Field(..., max_length=20)
    unites_vendues: int = Field(..., ge=0)


class CommercialDataSchema(CamelModel):
    """SENSIBLE — n'apparaît jamais dans une réponse vue client (voir RobotClientResponse)."""

    prix_catalogue_eur: float = Field(..., gt=0, alias="prixCatalogueEUR")
    remise_pct: float = Field(..., ge=0, le=100)
    quantite_stock: int = Field(..., ge=0)
    nombre_offres_en_cours: int = Field(..., ge=0)
    historique_ventes: list[VenteHistoriqueSchema] | None = None


# ---------------------------------------------------------------------------
# Réponses en lecture — deux vues strictement séparées (CDC §3.2 / §3.3)
# ---------------------------------------------------------------------------

class RobotClientResponse(CamelModel):
    """
    Vue Client (CDC §3.3) : aucune donnée commerciale. Ce schéma ne
    contient tout simplement PAS les champs `commercial` ni `statut` —
    l'omission structurelle est plus sûre qu'un filtrage à la volée
    (impossible d'oublier de masquer un champ ajouté plus tard).
    """

    id: str
    modele: str
    type: RobotType
    categorie: str
    annee_mise_en_service: int
    heures_utilisation: int
    description_courte: str
    caracteristiques: CaracteristiquesSchema
    prestations_disponibles: list[PrestationSchema]
    media: MediaSchema
    documentation: DocumentationSchema


class RobotCommercialResponse(RobotClientResponse):
    """Vue Commerciale (CDC §3.2) : ajoute les données sensibles + le statut de la fiche."""

    commercial: CommercialDataSchema
    statut: RobotStatut
    prix_final_eur: float = Field(..., alias="prixFinalEUR")


# ---------------------------------------------------------------------------
# Écriture — back-office RAN
# ---------------------------------------------------------------------------

class RobotCreate(CamelModel):
    """POST /robots (responsable_ran) — statut forcé à Brouillon côté service, jamais fourni par le client."""

    id: str = Field(..., min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_-]+$")
    modele: str = Field(..., min_length=1, max_length=150)
    type: RobotType
    categorie: str = Field(..., min_length=1, max_length=100)
    annee_mise_en_service: int = Field(..., ge=1990, le=2100)
    heures_utilisation: int = Field(..., ge=0)
    description_courte: str = Field(..., max_length=300)
    caracteristiques: CaracteristiquesSchema
    prestations_disponibles: list[PrestationSchema] = Field(default_factory=list)
    media: MediaSchema = Field(default_factory=MediaSchema)
    documentation: DocumentationSchema = Field(default_factory=DocumentationSchema)
    prix_catalogue_eur: float = Field(..., gt=0, alias="prixCatalogueEUR")
    remise_pct: float = Field(0, ge=0, le=100)
    quantite_stock: int = Field(0, ge=0)
    nombre_offres_en_cours: int = Field(0, ge=0)


class RobotUpdate(CamelModel):
    """PATCH /robots/{id} (responsable_ran) — tous champs optionnels, mise à jour partielle."""

    modele: str | None = Field(None, min_length=1, max_length=150)
    type: RobotType | None = None
    categorie: str | None = Field(None, min_length=1, max_length=100)
    annee_mise_en_service: int | None = Field(None, ge=1990, le=2100)
    heures_utilisation: int | None = Field(None, ge=0)
    description_courte: str | None = Field(None, max_length=300)
    caracteristiques: CaracteristiquesSchema | None = None
    prestations_disponibles: list[PrestationSchema] | None = None
    media: MediaSchema | None = None
    documentation: DocumentationSchema | None = None
    prix_catalogue_eur: float | None = Field(None, gt=0, alias="prixCatalogueEUR")
    remise_pct: float | None = Field(None, ge=0, le=100)
    quantite_stock: int | None = Field(None, ge=0)
    nombre_offres_en_cours: int | None = Field(None, ge=0)
    statut: RobotStatut | None = None
