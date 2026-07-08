from __future__ import annotations

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import models
from src.database import get_db
from src.security import decode_access_token
from src.shared.enums import UserRole
from src.shared.exceptions import ForbiddenError, UnauthorizedError

# `auto_error=False` : on gère nous-mêmes l'absence de token pour permettre
# les dépendances "optionnelles" (routes publiques dont le rendu dépend du
# rôle si un token est présent, ex: catalogue robots).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> models.User:
    """Exige un JWT d'accès valide. Lève 401 sinon."""
    if token is None:
        raise UnauthorizedError("Authentification requise.")

    payload = decode_access_token(token)
    if payload is None:
        raise UnauthorizedError("Jeton d'accès invalide ou expiré.")

    user_id = payload.get("sub")
    if user_id is None:
        raise UnauthorizedError("Jeton d'accès invalide.")

    user = await db.get(models.User, user_id)
    if user is None or not user.is_active:
        raise UnauthorizedError("Utilisateur introuvable ou désactivé.")

    return user


async def get_current_user_optional(
    token: str | None = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> models.User | None:
    """
    Variante permissive : renvoie `None` au lieu de lever une exception si
    aucun token (ou un token invalide) n'est présent. Utilisée par les
    routes accessibles à la fois en "vue client" anonyme et en "vue
    commerciale" authentifiée (CDC §5.2) — le filtrage des champs sensibles
    se fait ensuite dans la couche service selon la présence/le rôle de
    l'utilisateur, jamais côté client.
    """
    if token is None:
        return None
    payload = decode_access_token(token)
    if payload is None:
        return None
    user_id = payload.get("sub")
    if user_id is None:
        return None
    user = await db.get(models.User, user_id)
    if user is None or not user.is_active:
        return None
    return user


def require_roles(*roles: UserRole):
    """
    Factory de dépendance : `Depends(require_roles(UserRole.RESPONSABLE_RAN))`.
    Sépare strictement les droits par rôle (CDC §4.3) — un commercial ne
    peut jamais atteindre une route réservée au back-office RAN et
    inversement, quel que soit ce qu'affiche le frontend.
    """

    async def _dependency(current_user: models.User = Depends(get_current_user)) -> models.User:
        if current_user.role not in roles:
            raise ForbiddenError("Vous n'avez pas les droits nécessaires pour cette action.")
        return current_user

    return _dependency
