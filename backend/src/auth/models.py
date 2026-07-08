from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, ForeignKey, String #type: ignore
from sqlalchemy.orm import Mapped, mapped_column, relationship #type: ignore

from src.database import TABLE_PREFIX, Base
from src.shared.enums import UserRole


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    """
    Compte utilisateur — uniquement les rôles authentifiés (commercial,
    responsable_ran). La "vue client" du CDC n'a pas de compte : elle est
    soit anonyme, soit un mode d'affichage d'un commercial connecté.
    """

    __tablename__ = f"{TABLE_PREFIX}users"
    

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    nom: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, native_enum=False, length=32))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    failed_login_attempts: Mapped[int] = mapped_column(default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class RefreshToken(Base):
    """
    Refresh tokens actifs, stockés hachés (jamais en clair). Permet la
    révocation individuelle (logout) ou globale (changement de mot de passe,
    compromission suspectée) sans attendre l'expiration naturelle.
    """

    __tablename__ = f"{TABLE_PREFIX}refresh_tokens"
    

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey(f"{TABLE_PREFIX}users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")
