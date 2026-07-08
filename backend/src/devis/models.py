from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Enum as SQLEnum, ForeignKey, String, Text #type: ignore
from sqlalchemy.orm import Mapped, mapped_column, relationship #type: ignore

from src.database import TABLE_PREFIX, Base
from src.shared.enums import NiveauRenovation


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class DevisRequest(Base):
    """Demande de devis (CDC §3.5) — aligné sur `DevisRequest` (frontend/src/types/devis.types.ts)."""

    __tablename__ = f"{TABLE_PREFIX}devis_requests"
    __table_args__ = {'schema': 'dbo'}

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    reference: Mapped[str] = mapped_column(String(30), unique=True, index=True)

    prenom: Mapped[str] = mapped_column(String(100))
    nom: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), index=True)
    telephone: Mapped[str] = mapped_column(String(30))
    pays: Mapped[str] = mapped_column(String(100))
    societe: Mapped[str | None] = mapped_column(String(150), nullable=True)
    fonction: Mapped[str | None] = mapped_column(String(150), nullable=True)

    robot_id: Mapped[str | None] = mapped_column(ForeignKey(f"{TABLE_PREFIX}robots.id", ondelete="SET NULL"), nullable=True, index=True)
    demande_speciale: Mapped[str | None] = mapped_column(Text, nullable=True)

    commercial_assigne: Mapped[str] = mapped_column(String(150))
    envoye_le: Mapped[datetime] = mapped_column(default=_utcnow)

    prestations_souhaitees: Mapped[list["DevisPrestationSouhaitee"]] = relationship(back_populates="devis", cascade="all, delete-orphan")


class DevisPrestationSouhaitee(Base):
    __tablename__ = f"{TABLE_PREFIX}devis_prestations_souhaitees"
    __table_args__ = {'schema': 'dbo'}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    devis_id: Mapped[str] = mapped_column(ForeignKey(f"{TABLE_PREFIX}devis_requests.id", ondelete="CASCADE"), index=True)
    niveau: Mapped[NiveauRenovation] = mapped_column(SQLEnum(NiveauRenovation, native_enum=False, length=32))

    devis: Mapped["DevisRequest"] = relationship(back_populates="prestations_souhaitees")
