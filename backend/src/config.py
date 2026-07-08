"""
Configuration globale de l'application.

Toutes les valeurs sensibles (clé secrète, URL de base de données...) sont
lues depuis l'environnement / le fichier `.env` — jamais codées en dur dans
le dépôt. `SECRET_KEY` DOIT être surchargée en production : la valeur par
défaut ci-dessous ne sert qu'à ce que l'application démarre en développement
sans configuration préalable, et déclenche un avertissement explicite.
"""
from __future__ import annotations

import json
import secrets
import warnings
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ENVIRONMENT: str = "development"

    DATABASE_URL: str = "sqlite+aiosqlite:///./ran_catalogue.db"

    SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 480  # 8h, aligné sur une journée de travail (cf. frontend)

    CORS_ORIGINS: str = '["http://localhost:5173","http://127.0.0.1:5173"]'

    COOKIE_SECURE: bool = False
    REFRESH_COOKIE_NAME: str = "ran_refresh_token"

    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 10
    MAX_IMPORT_ROWS: int = 500

    LOGIN_RATE_LIMIT: str = "5/minute"

    @property
    def cors_origins_list(self) -> list[str]:
        try:
            parsed = json.loads(self.CORS_ORIGINS)
            if isinstance(parsed, list):
                return [str(o) for o in parsed]
        except (json.JSONDecodeError, TypeError):
            pass
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() in {"production", "prod"}


@lru_cache
def get_settings() -> Settings:
    settings = Settings()

    if not settings.SECRET_KEY:
        if settings.is_production:
            raise RuntimeError(
                "SECRET_KEY est obligatoire en production. "
                "Générez-en une avec `python -c \"import secrets; print(secrets.token_urlsafe(64))\"` "
                "et définissez-la dans l'environnement / le fichier .env."
            )
        # Dev uniquement : clé éphémère générée à chaque démarrage pour que
        # l'app fonctionne sans configuration, tout en évitant une clé fixe
        # partagée par tout le monde dans le code source.
        settings.SECRET_KEY = secrets.token_urlsafe(64)
        warnings.warn(
            "SECRET_KEY absente de l'environnement : une clé aléatoire éphémère a été "
            "générée pour ce process (dev uniquement). Toutes les sessions seront "
            "invalidées au redémarrage. Définissez SECRET_KEY dans .env pour la persistance.",
            stacklevel=2,
        )

    if settings.is_production and not settings.COOKIE_SECURE:
        raise RuntimeError("COOKIE_SECURE doit être True en production (cookies transmis en HTTPS uniquement).")

    return settings


settings = get_settings()
