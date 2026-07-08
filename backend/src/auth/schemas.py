from __future__ import annotations

from pydantic import EmailStr, Field #type: ignore

from src.shared.enums import UserRole
from src.shared.schemas import CamelModel


class Credentials(CamelModel):
    """Aligné sur `Credentials` (frontend/src/types/user.types.ts)."""

    email: EmailStr
    password: str = Field(..., min_length=1, max_length=200)


class AuthenticatedUser(CamelModel):
    """Aligné sur `AuthenticatedUser` (frontend) — jamais de champ mot de passe."""

    id: str
    nom: str
    email: EmailStr
    role: UserRole


class AccessTokenResponse(CamelModel):
    """
    Réponse de /auth/login et /auth/refresh. Le refresh token n'apparaît
    JAMAIS dans ce corps de réponse JSON : il est posé en cookie httpOnly
    par le serveur (voir router.py), donc invisible et inaccessible au JS
    du frontend — c'est la principale amélioration de sécurité par rapport
    au mock (qui stockait tout, y compris la session, en sessionStorage).
    """

    access_token: str
    token_type: str = "bearer"
    expires_in: int  # secondes
    user: AuthenticatedUser


class UserCreate(CamelModel):
    """Réservé à un provisioning interne (script de seed / admin) — pas de route d'auto-inscription publique."""

    nom: str = Field(..., min_length=1, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=10, max_length=200)
    role: UserRole
