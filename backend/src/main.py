"""
Point d'entrée de l'application — Catalogue robots FANUC reconditionnés (RAN).

Création automatique de la base de données : au démarrage (`lifespan`),
`Base.metadata.create_all` crée toutes les tables déclarées par les modèles
SQLAlchemy de chaque domaine (auth, robots, coming_soon, devis, imports).
Ces modèles sont le pendant "persistance" des schémas Pydantic exposés par
l'API (voir `schemas.py` de chaque domaine) — les deux sont synchronisés à
la main par design (séparation des responsabilités), pas par génération
automatique de l'un à partir de l'autre.

En développement (SQLite), ce mécanisme suffit. En production, il est
recommandé de migrer vers Alembic pour des migrations versionnées et
réversibles plutôt que `create_all` (voir README.md).
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request #type: ignore
from fastapi.middleware.cors import CORSMiddleware #type: ignore
from slowapi import _rate_limit_exceeded_handler #type: ignore
from slowapi.errors import RateLimitExceeded #type: ignore
from slowapi.middleware import SlowAPIMiddleware #type: ignore

from src.auth.router import limiter as auth_limiter
from src.auth.router import router as auth_router
from src.coming_soon.router import router as coming_soon_router
from src.config import settings
from src.database import Base, engine
from src.devis.router import limiter as devis_limiter
from src.devis.router import router as devis_router
from src.imports.router import router as imports_router
from src.robots.router import router as robots_router
from src.shared.exceptions import register_exception_handlers

# Import explicite de tous les modules `models` : nécessaire pour que
# `Base.metadata` connaisse toutes les tables avant `create_all`, même si
# les modèles ne sont pas référencés directement ici.
from src.auth import models as _auth_models  # noqa: F401
from src.robots import models as _robot_models  # noqa: F401
from src.coming_soon import models as _coming_soon_models  # noqa: F401
from src.devis import models as _devis_models  # noqa: F401
from src.imports import models as _import_models  # noqa: F401

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ran_catalogue")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Base de données initialisée (tables créées si absentes).")
    yield
    await engine.dispose()


app = FastAPI(
    title="RAN Catalogue API",
    description="API back-end du catalogue de robots FANUC reconditionnés (RAN).",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

# --- Rate limiting (anti brute-force / anti-spam sur /auth/login et /devis) ---
app.state.limiter = auth_limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# --- CORS : liste blanche stricte d'origines, credentials nécessaires pour le cookie refresh ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    """En-têtes de sécurité standards, appliqués à toutes les réponses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if settings.is_production:
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    return response


app.include_router(auth_router)
app.include_router(robots_router)
app.include_router(coming_soon_router)
app.include_router(devis_router)
app.include_router(imports_router)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
