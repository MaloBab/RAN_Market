from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select #type: ignore
from sqlalchemy.ext.asyncio import AsyncSession #type: ignore

from src.auth import models, schemas
from src.config import settings
from src.security import (create_access_token, generate_refresh_token, hash_refresh_token, verify_password)
from src.shared.exceptions import UnauthorizedError

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION = timedelta(minutes=15)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _as_aware(dt: datetime) -> datetime:
    """
    SQLite ne conserve pas l'information de fuseau horaire (contrairement à
    PostgreSQL) : une valeur stockée en UTC en ressort "naive" à la
    relecture. On la re-marque explicitement comme UTC pour pouvoir la
    comparer sans erreur à un datetime aware, quel que soit le moteur de
    base de données utilisé.
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


async def authenticate(db: AsyncSession, credentials: schemas.Credentials) -> models.User:
    """
    Vérifie les identifiants. Toujours exécuter un hachage même si l'email
    est inconnu (protection contre l'énumération de comptes par mesure de
    timing) et renvoyer un message d'erreur générique et identique dans
    tous les cas d'échec.
    """
    result = await db.execute(select(models.User).where(models.User.email == credentials.email.lower()))
    user = result.scalar_one_or_none()

    # Dummy hash utilisé quand l'utilisateur n'existe pas, pour que
    # verify_password() prenne un temps comparable dans les deux branches.
    dummy_hash = "$2b$12$CwaJek1cZUt1Wp1n9tvKz.gJPr6bMHVCu6TDXTvpjRGfbA0BwR6Xa"

    if user is None:
        verify_password(credentials.password, dummy_hash)
        raise UnauthorizedError("Identifiants incorrects.")

    if user.locked_until and _as_aware(user.locked_until) > _utcnow():
        raise UnauthorizedError("Compte temporairement verrouillé suite à plusieurs échecs de connexion. Réessayez plus tard.")

    if not user.is_active:
        raise UnauthorizedError("Ce compte est désactivé.")

    if not verify_password(credentials.password, user.hashed_password):
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
            user.locked_until = _utcnow() + LOCKOUT_DURATION
            user.failed_login_attempts = 0
        await db.commit()
        raise UnauthorizedError("Identifiants incorrects.")

    if user.failed_login_attempts:
        user.failed_login_attempts = 0
        user.locked_until = None
        await db.commit()

    return user


async def issue_tokens(db: AsyncSession, user: models.User) -> tuple[str, str, int]:
    """Retourne (access_token, refresh_token_en_clair, expires_in_secondes)."""
    access_token = create_access_token(subject=user.id, role=user.role.value)

    refresh_plain = generate_refresh_token()
    refresh_token = models.RefreshToken(
        id=str(uuid.uuid4()),
        user_id=user.id,
        token_hash=hash_refresh_token(refresh_plain),
        expires_at=_utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))
    db.add(refresh_token)
    await db.commit()

    return access_token, refresh_plain, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60


async def rotate_refresh_token(db: AsyncSession, refresh_token_plain: str) -> tuple[str, str, int, models.User]:
    """
    Vérifie un refresh token présenté (cookie httpOnly), le révoque, et en
    émet un nouveau (rotation) + un nouvel access token. La rotation limite
    la fenêtre d'exploitation si un refresh token venait à fuiter.
    """
    token_hash = hash_refresh_token(refresh_token_plain)
    result = await db.execute(select(models.RefreshToken).where(models.RefreshToken.token_hash == token_hash))
    stored = result.scalar_one_or_none()

    if stored is None or stored.revoked or _as_aware(stored.expires_at) < _utcnow():
        raise UnauthorizedError("Session expirée, veuillez vous reconnecter.")

    user = await db.get(models.User, stored.user_id)
    if user is None or not user.is_active:
        raise UnauthorizedError("Session expirée, veuillez vous reconnecter.")

    stored.revoked = True
    await db.commit()

    access_token, new_refresh_token, expires_in = await issue_tokens(db, user)
    return access_token, new_refresh_token, expires_in, user


async def revoke_refresh_token(db: AsyncSession, refresh_token_plain: str) -> None:
    token_hash = hash_refresh_token(refresh_token_plain)
    result = await db.execute(select(models.RefreshToken).where(models.RefreshToken.token_hash == token_hash))
    stored = result.scalar_one_or_none()
    if stored is not None:
        stored.revoked = True
        await db.commit()


async def revoke_all_user_tokens(db: AsyncSession, user_id: str) -> None:
    result = await db.execute(
        select(models.RefreshToken).where(models.RefreshToken.user_id == user_id, models.RefreshToken.revoked.is_(False)))
    for token in result.scalars().all():
        token.revoked = True
    await db.commit()
