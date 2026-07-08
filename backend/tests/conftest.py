from __future__ import annotations

import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production-use-only-in-ci")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("COOKIE_SECURE", "false")
# Limite haute en test : le test de verrouillage de compte enchaîne 6
# requêtes de login consécutives et ne doit pas être bloqué par le
# rate-limiter applicatif (qui reste actif en développement/production).
os.environ.setdefault("LOGIN_RATE_LIMIT", "1000/minute")

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.auth.router import limiter as _auth_limiter
from src.devis.router import limiter as _devis_limiter


@pytest.fixture(autouse=True)
def _reset_rate_limiters():
    """Le state du limiter est un singleton process-wide : on le vide avant
    chaque test pour ne pas faire échouer un test à cause d'un précédent."""
    _auth_limiter.reset()
    _devis_limiter.reset()
    yield
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from src.database import Base, get_db
from src.main import app
from src.security import hash_password
from src.shared.enums import UserRole


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def _override_get_db():
        async with session_factory() as session:
            yield session
            await session.commit()

    app.dependency_overrides[get_db] = _override_get_db

    async with session_factory() as session:
        yield session

    app.dependency_overrides.clear()
    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def commercial_user(db_session: AsyncSession):
    from src.auth.models import User

    user = User(
        id="usr-commercial", nom="Camille Berthier", email="commercial@fanuc-ran.example",
        hashed_password=hash_password("Commercial#2026"), role=UserRole.COMMERCIAL, is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    return user


@pytest_asyncio.fixture
async def responsable_user(db_session: AsyncSession):
    from src.auth.models import User

    user = User(
        id="usr-responsable", nom="Julien Ferreira", email="responsable@fanuc-ran.example",
        hashed_password=hash_password("ResponsableRAN#2026"), role=UserRole.RESPONSABLE_RAN, is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    return user


async def _login(client: AsyncClient, email: str, password: str) -> str:
    response = await client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["accessToken"]


@pytest_asyncio.fixture
async def commercial_token(client: AsyncClient, commercial_user):
    return await _login(client, "commercial@fanuc-ran.example", "Commercial#2026")


@pytest_asyncio.fixture
async def responsable_token(client: AsyncClient, responsable_user):
    return await _login(client, "responsable@fanuc-ran.example", "ResponsableRAN#2026")
