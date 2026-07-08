from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import TABLE_PREFIX, Base
from src.shared.enums import ImportRowStatus


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ImportBatch(Base):
    """
    Trace un import Excel back-office (CDC §3.6) — conservé pour audit
    (qui a importé quoi, quand, avec quel résultat). Aligné sur
    `ImportReport` (frontend/src/types/import.types.ts).
    """

    __tablename__ = f"{TABLE_PREFIX}import_batches"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    operator_id: Mapped[str] = mapped_column(ForeignKey(f"{TABLE_PREFIX}users.id", ondelete="SET NULL"), nullable=True)
    filename: Mapped[str] = mapped_column(String(255))
    total_lignes: Mapped[int] = mapped_column(Integer)
    accepte: Mapped[int] = mapped_column(Integer)
    erreurs: Mapped[int] = mapped_column(Integer)
    doublons: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    details: Mapped[list["ImportRowResult"]] = relationship(
        back_populates="batch", cascade="all, delete-orphan", order_by="ImportRowResult.ligne"
    )


class ImportRowResult(Base):
    __tablename__ = f"{TABLE_PREFIX}import_row_results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    batch_id: Mapped[str] = mapped_column(ForeignKey(f"{TABLE_PREFIX}import_batches.id", ondelete="CASCADE"), index=True)
    ligne: Mapped[int] = mapped_column(Integer)
    id_robot: Mapped[str] = mapped_column(String(50))
    statut: Mapped[ImportRowStatus] = mapped_column(SQLEnum(ImportRowStatus, native_enum=False, length=20))
    message: Mapped[str | None] = mapped_column(String(500), nullable=True)

    batch: Mapped["ImportBatch"] = relationship(back_populates="details")
