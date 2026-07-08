"""
Exceptions métier communes + handlers globaux.

Objectif sécurité : ne jamais laisser fuiter une trace Python brute au
client (stack trace, chemin de fichier, requête SQL...). Toute exception
non prévue est journalisée côté serveur et renvoyée au client sous une
forme générique.
"""
from __future__ import annotations

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger("ran_catalogue")


class AppError(Exception):
    """Base pour toutes les erreurs métier volontairement remontées à l'API."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Erreur inconnue."

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.detail
        super().__init__(self.detail)


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Ressource introuvable."


class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Conflit avec une ressource existante."


class ForbiddenError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Accès refusé."


class UnauthorizedError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authentification requise ou invalide."


class InvalidFileError(AppError):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    detail = "Fichier invalide."


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        # On renvoie les erreurs de validation Pydantic mais jamais le corps brut de
        # la requête (peut contenir un mot de passe en clair sur /auth/login par ex.).
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Erreur non gérée sur %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Une erreur interne est survenue."},
        )
