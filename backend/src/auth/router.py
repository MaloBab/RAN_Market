from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import schemas, service
from src.auth.dependencies import get_current_user
from src.auth.models import User
from src.config import settings
from src.database import get_db
from src.shared.exceptions import UnauthorizedError

router = APIRouter(prefix="/auth", tags=["auth"])

limiter = Limiter(key_func=get_remote_address)


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    """
    Cookie httpOnly + Secure (en prod) + SameSite=strict : inaccessible en
    JS (protège contre le vol via XSS) et non transmis lors de requêtes
    cross-site (protège contre le CSRF classique sur ce cookie).
    """
    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        path="/auth",
    )


def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(key=settings.REFRESH_COOKIE_NAME, path="/auth")


@router.post("/login", response_model=schemas.AccessTokenResponse)
@limiter.limit(settings.LOGIN_RATE_LIMIT)
async def login(
    request: Request,
    response: Response,
    credentials: schemas.Credentials,
    db: AsyncSession = Depends(get_db),
) -> schemas.AccessTokenResponse:
    """
    POST /auth/login — vérifie les identifiants côté serveur (hash bcrypt),
    émet un JWT d'accès de courte durée dans le corps de la réponse et un
    refresh token opaque dans un cookie httpOnly. Limité par IP pour
    ralentir le brute-force (`LOGIN_RATE_LIMIT`, 5/minute par défaut).
    """
    user = await service.authenticate(db, credentials)
    access_token, refresh_token, expires_in = await service.issue_tokens(db, user)
    _set_refresh_cookie(response, refresh_token)

    return schemas.AccessTokenResponse(
        access_token=access_token,
        expires_in=expires_in,
        user=schemas.AuthenticatedUser.model_validate(user),
    )


@router.post("/refresh", response_model=schemas.AccessTokenResponse)
async def refresh(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> schemas.AccessTokenResponse:
    """POST /auth/refresh — lit le cookie httpOnly, effectue une rotation du refresh token."""
    refresh_token = request.cookies.get(settings.REFRESH_COOKIE_NAME)
    if not refresh_token:
        raise UnauthorizedError("Aucune session active.")

    access_token, new_refresh_token, expires_in, user = await service.rotate_refresh_token(db, refresh_token)
    _set_refresh_cookie(response, new_refresh_token)

    return schemas.AccessTokenResponse(
        access_token=access_token,
        expires_in=expires_in,
        user=schemas.AuthenticatedUser.model_validate(user),
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> None:
    """POST /auth/logout — révoque le refresh token courant et efface le cookie."""
    refresh_token = request.cookies.get(settings.REFRESH_COOKIE_NAME)
    if refresh_token:
        await service.revoke_refresh_token(db, refresh_token)
    _clear_refresh_cookie(response)


@router.get("/me", response_model=schemas.AuthenticatedUser)
async def get_me(current_user: User = Depends(get_current_user)) -> schemas.AuthenticatedUser:
    """GET /auth/me — revalide le token courant et renvoie l'utilisateur (équivalent getSession)."""
    return schemas.AuthenticatedUser.model_validate(current_user)
