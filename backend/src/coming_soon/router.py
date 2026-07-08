from __future__ import annotations

from fastapi import APIRouter, Depends #type: ignore
from sqlalchemy import select #type: ignore
from sqlalchemy.ext.asyncio import AsyncSession #type: ignore

from src.auth.dependencies import require_roles
from src.auth.models import User
from src.coming_soon import models, schemas
from src.database import get_db
from src.shared.enums import UserRole
from src.shared.exceptions import ConflictError, NotFoundError

router = APIRouter(prefix="/coming-soon", tags=["coming-soon"])


@router.get("", response_model=list[schemas.ComingSoonResponse])
async def list_coming_soon(current_user: User = Depends(require_roles(UserRole.COMMERCIAL, UserRole.RESPONSABLE_RAN)), db: AsyncSession = Depends(get_db)):
    """GET /coming-soon — CDC §3.7 : vue commerciale uniquement, jamais accessible côté client anonyme."""
    result = await db.execute(select(models.ComingSoonEntry).order_by(models.ComingSoonEntry.created_at.desc()))
    return list(result.scalars().all())


@router.post("", response_model=schemas.ComingSoonResponse, status_code=201)
async def create_coming_soon_entry(payload: schemas.ComingSoonCreate, current_user: User = Depends(require_roles(UserRole.RESPONSABLE_RAN)), db: AsyncSession = Depends(get_db)):
    existing = await db.get(models.ComingSoonEntry, payload.id)
    if existing is not None:
        raise ConflictError(f"Une entrée Coming Soon avec l'ID {payload.id} existe déjà.")
    entry = models.ComingSoonEntry(**payload.model_dump())
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


@router.patch("/{entry_id}", response_model=schemas.ComingSoonResponse)
async def update_coming_soon_entry(
    entry_id: str,
    payload: schemas.ComingSoonUpdate,
    current_user: User = Depends(require_roles(UserRole.RESPONSABLE_RAN)),
    db: AsyncSession = Depends(get_db),
):
    entry = await db.get(models.ComingSoonEntry, entry_id)
    if entry is None:
        raise NotFoundError(f"Entrée Coming Soon '{entry_id}' introuvable.")
    for field_name, value in payload.model_dump(exclude_unset=True).items():
        setattr(entry, field_name, value)
    await db.commit()
    await db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=204)
async def delete_coming_soon_entry(entry_id: str, current_user: User = Depends(require_roles(UserRole.RESPONSABLE_RAN)), db: AsyncSession = Depends(get_db)):
    entry = await db.get(models.ComingSoonEntry, entry_id)
    if entry is None:
        raise NotFoundError(f"Entrée Coming Soon '{entry_id}' introuvable.")
    await db.delete(entry)
    await db.commit()
