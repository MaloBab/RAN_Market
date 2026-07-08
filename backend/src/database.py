"""
Connexion base de données — SQLAlchemy 2.0 async.

La création des tables est faite automatiquement au démarrage de
l'application (voir `main.py` → lifespan) à partir des modèles déclarés
dans chaque domaine (`Base.metadata.create_all`). Chaque modèle SQLAlchemy
est le pendant "persistance" d'un schéma Pydantic équivalent dans
`schemas.py` du même domaine ; les deux sont volontairement séparés
(DIP / séparation des responsabilités), la conversion se faisant via
`model_config = ConfigDict(from_attributes=True)` côté Pydantic.
"""
from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine #type: ignore
from sqlalchemy.orm import DeclarativeBase #type: ignore
from sqlalchemy import MetaData #type: ignore

from src.config import settings

TABLE_PREFIX = "ranmarket_"
DB_SCHEMA = "dbo"
metadata_obj = MetaData(schema=DB_SCHEMA)

engine_kwargs: dict = {"echo": False}

if settings.DATABASE_URL.startswith("sqlite"):
    # Nécessaire pour SQLite + async (une seule connexion partagée par défaut).
    engine_kwargs["connect_args"] = {"check_same_thread": False}
elif settings.DATABASE_URL.startswith("mssql"):
    # Azure SQL peut fermer une connexion inactive (pause serverless, load
    # balancer, etc.) : `pool_pre_ping` détecte une connexion morte et la
    # remplace avant de l'utiliser plutôt que de faire échouer la requête,
    # et `pool_recycle` la renouvelle proactivement avant qu'Azure ne le
    # fasse elle-même (timeout par défaut de 30 min côté serveur).
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_recycle"] = 1800

engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)

async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    metadata = metadata_obj


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dépendance FastAPI : fournit une session par requête, commit/rollback automatiques."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
