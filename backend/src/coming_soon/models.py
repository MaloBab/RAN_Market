from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Enum as SQLEnum, String #type: ignore
from sqlalchemy.orm import Mapped, mapped_column #type: ignore

from src.database import TABLE_PREFIX, Base
from src.shared.enums import NiveauRenovation, RobotType


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ComingSoonEntry(Base):
    """Aligné sur `ComingSoonEntry` (frontend/src/types/robot.types.ts) — CDC §3.7."""

    __tablename__ = f"{TABLE_PREFIX}coming_soon_entries"
    __table_args__ = {'schema': 'dbo'}

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    modele: Mapped[str] = mapped_column(String(150))
    type: Mapped[RobotType] = mapped_column(SQLEnum(RobotType, native_enum=False, length=32))
    disponibilite_estimee: Mapped[str] = mapped_column(String(30))  # ex: "T1 2027"
    niveau_renovation_prevu: Mapped[NiveauRenovation] = mapped_column(SQLEnum(NiveauRenovation, native_enum=False, length=32))
    created_at: Mapped[datetime] = mapped_column(default=_utcnow)
