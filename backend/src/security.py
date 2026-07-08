"""
Primitives de sécurité partagées entre domaines.

- Hachage des mots de passe : passlib/bcrypt (jamais de mot de passe en clair
  stocké ou journalisé, coût adaptatif bcrypt).
- JWT d'accès : courte durée de vie (15 min par défaut), signé HS256 avec
  `SECRET_KEY`, transporté en Authorization Bearer (jamais en cookie —
  évite le CSRF sur ce token).
- Refresh token : chaîne aléatoire opaque (pas un JWT) stockée hachée
  (SHA-256) en base, transportée en cookie httpOnly + Secure + SameSite=strict.
  Le fait de le stocker haché signifie qu'une fuite de la base ne permet
  pas de rejouer les tokens existants (comme un mot de passe).
"""
from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------------------------------------------------------------------
# Mots de passe
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Comparaison en temps constant assurée par passlib (protège contre les
    attaques par mesure de timing)."""
    return pwd_context.verify(plain_password, hashed_password)


# ---------------------------------------------------------------------------
# JWT d'accès
# ---------------------------------------------------------------------------

def create_access_token(*, subject: str, role: str, extra_claims: dict | None = None) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "role": role,
        "iat": now,
        "exp": expire,
        "type": "access",
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None
    if payload.get("type") != "access":
        return None
    return payload


# ---------------------------------------------------------------------------
# Refresh token opaque
# ---------------------------------------------------------------------------

def generate_refresh_token() -> str:
    """Token aléatoire cryptographiquement sûr (256 bits d'entropie encodés en URL-safe)."""
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    """SHA-256 suffit ici : le token est déjà à haute entropie (pas un mot de
    passe humain), on veut juste éviter de stocker le secret en clair en base."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
