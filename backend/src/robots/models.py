from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Enum as SQLEnum, Float, ForeignKey, Integer, String #type: ignore
from sqlalchemy.orm import Mapped, mapped_column, relationship #type: ignore

from src.database import TABLE_PREFIX, Base
from src.shared.enums import BaieType, NiveauRenovation, RobotStatut, RobotType


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Robot(Base):
    """
    Fiche robot — aligné sur `Robot` (frontend/src/types/robot.types.ts).

    Les données strictement commerciales (`prix_catalogue_eur`, `remise_pct`,
    `quantite_stock`, `nombre_offres_en_cours`) sont inline ici plutôt que
    dans une table séparée (relation 1:1 stricte) mais NE SONT JAMAIS
    sérialisées dans la réponse "vue client" — voir `robots/schemas.py`
    (`RobotClientResponse` ne les expose pas du tout) et `robots/service.py`
    qui choisit le schéma de sortie selon le rôle de l'appelant, côté
    serveur uniquement (CDC §4.3, §5.2).
    """

    __tablename__ = f"{TABLE_PREFIX}robots"
    

    id: Mapped[str] = mapped_column(String(50), primary_key=True)  # ex: FANUC-2024-001
    modele: Mapped[str] = mapped_column(String(150))
    type: Mapped[RobotType] = mapped_column(SQLEnum(RobotType, native_enum=False, length=32))
    categorie: Mapped[str] = mapped_column(String(100))
    annee_mise_en_service: Mapped[int] = mapped_column(Integer)
    heures_utilisation: Mapped[int] = mapped_column(Integer)
    description_courte: Mapped[str] = mapped_column(String(300))
    statut: Mapped[RobotStatut] = mapped_column(
        SQLEnum(RobotStatut, native_enum=False, length=32), default=RobotStatut.BROUILLON
    )

    # Caractéristiques techniques (RobotCaracteristiques)
    payload_kg: Mapped[float] = mapped_column(Float)
    rayon_action_mm: Mapped[int] = mapped_column(Integer)
    axes: Mapped[int] = mapped_column(Integer)
    type_baie: Mapped[BaieType] = mapped_column(SQLEnum(BaieType, native_enum=False, length=32))
    protection_ip: Mapped[str] = mapped_column(String(30))
    montage: Mapped[str] = mapped_column(String(100))

    # Documentation (RobotDocumentation)
    datasheet_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    flyer_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    brochure_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Media (RobotMedia) — vidéo inline, photos/galerie en tables associées
    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Données commerciales (RobotDonneesCommerciales) — SENSIBLES, jamais en vue client
    prix_catalogue_eur: Mapped[float] = mapped_column(Float)
    remise_pct: Mapped[float] = mapped_column(Float, default=0)
    quantite_stock: Mapped[int] = mapped_column(Integer, default=0)
    nombre_offres_en_cours: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=_utcnow, onupdate=_utcnow)

    prestations: Mapped[list["RobotPrestation"]] = relationship(
        back_populates="robot", cascade="all, delete-orphan", order_by="RobotPrestation.id"
    )
    photos_avant: Mapped[list["RobotPhoto"]] = relationship(
        back_populates="robot", cascade="all, delete-orphan", order_by="RobotPhoto.ordre"
    )
    galerie_avant_apres: Mapped[list["RobotGalerieItem"]] = relationship(
        back_populates="robot", cascade="all, delete-orphan", order_by="RobotGalerieItem.id"
    )
    historique_ventes: Mapped[list["RobotVenteHistorique"]] = relationship(
        back_populates="robot", cascade="all, delete-orphan", order_by="RobotVenteHistorique.periode"
    )


class RobotPrestation(Base):
    """Niveaux de rénovation disponibles pour une fiche (PrestationRenovation)."""

    __tablename__ = f"{TABLE_PREFIX}robot_prestations"
    

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    robot_id: Mapped[str] = mapped_column(ForeignKey(f"{TABLE_PREFIX}robots.id", ondelete="CASCADE"), index=True)
    niveau: Mapped[NiveauRenovation] = mapped_column(SQLEnum(NiveauRenovation, native_enum=False, length=32))
    garantie_mois: Mapped[int | None] = mapped_column(Integer, nullable=True)  # None = "à définir"

    robot: Mapped["Robot"] = relationship(back_populates="prestations")


class RobotPhoto(Base):
    """Photos avant rénovation (RobotMedia.photosAvant)."""

    __tablename__ = f"{TABLE_PREFIX}robot_photos"
    

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    robot_id: Mapped[str] = mapped_column(ForeignKey(f"{TABLE_PREFIX}robots.id", ondelete="CASCADE"), index=True)
    url: Mapped[str] = mapped_column(String(500))
    ordre: Mapped[int] = mapped_column(Integer, default=0)

    robot: Mapped["Robot"] = relationship(back_populates="photos_avant")


class RobotGalerieItem(Base):
    """Paires avant/après (RobotMedia.galerieAvantApres)."""

    __tablename__ = f"{TABLE_PREFIX}robot_galerie_items"
    

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    robot_id: Mapped[str] = mapped_column(ForeignKey(f"{TABLE_PREFIX}robots.id", ondelete="CASCADE"), index=True)
    avant_url: Mapped[str] = mapped_column(String(500))
    apres_url: Mapped[str] = mapped_column(String(500))
    legende: Mapped[str | None] = mapped_column(String(200), nullable=True)

    robot: Mapped["Robot"] = relationship(back_populates="galerie_avant_apres")


class RobotVenteHistorique(Base):
    """Historique de ventes — visible uniquement en vue commerciale ("si applicable", CDC §2.1)."""

    __tablename__ = f"{TABLE_PREFIX}robot_ventes_historique"
    

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    robot_id: Mapped[str] = mapped_column(ForeignKey(f"{TABLE_PREFIX}robots.id", ondelete="CASCADE"), index=True)
    periode: Mapped[str] = mapped_column(String(20))  # ex: "2026-Q1"
    unites_vendues: Mapped[int] = mapped_column(Integer)

    robot: Mapped["Robot"] = relationship(back_populates="historique_ventes")
