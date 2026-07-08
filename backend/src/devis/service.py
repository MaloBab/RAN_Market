from __future__ import annotations

import secrets
import uuid
from datetime import datetime, timezone

from sqlalchemy import func, select #type: ignore
from sqlalchemy.ext.asyncio import AsyncSession #type: ignore
from sqlalchemy.orm import selectinload #type: ignore

from src.auth.models import User
from src.devis import models, schemas
from src.shared.enums import UserRole
from src.shared.exceptions import AppError


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _generate_reference() -> str:
    year = _utcnow().year
    suffix = secrets.token_hex(3).upper()
    return f"DEV-{year}-{suffix}"


async def _pick_commercial(db: AsyncSession) -> User:
    """
    Répartition round-robin simple : le commercial actif ayant le moins de
    devis déjà assignés reçoit la nouvelle demande. Évite qu'un seul
    commercial soit systématiquement surchargé.
    """
    result = await db.execute(
        select(User, func.count(models.DevisRequest.id).label("nb_devis"))
        .outerjoin( models.DevisRequest, models.DevisRequest.commercial_assigne == User.nom)
        .where(User.role == UserRole.COMMERCIAL, User.is_active.is_(True))
        .group_by(User.id)
        .order_by("nb_devis")
    )
    row = result.first()
    if row is None:
        raise AppError("Aucun commercial disponible pour traiter la demande actuellement.")
    return row[0]


async def create_devis_request(db: AsyncSession, payload: schemas.DevisRequestCreate) -> models.DevisRequest:
    commercial = await _pick_commercial(db)

    devis = models.DevisRequest(
        id=str(uuid.uuid4()),
        reference=_generate_reference(),
        prenom=payload.prenom,
        nom=payload.nom,
        email=payload.email,
        telephone=payload.telephone,
        pays=payload.pays,
        societe=payload.societe,
        fonction=payload.fonction,
        robot_id=payload.robot_id,
        demande_speciale=payload.demande_speciale,
        commercial_assigne=commercial.nom)
    devis.prestations_souhaitees = [models.DevisPrestationSouhaitee(niveau=n) for n in payload.prestations_souhaitees]
    db.add(devis)
    await db.commit()
    await db.refresh(devis, attribute_names=["prestations_souhaitees"])
    return devis


async def list_devis_requests(db: AsyncSession) -> list[models.DevisRequest]:
    

    stmt = (
        select(models.DevisRequest)
        .options(selectinload(models.DevisRequest.prestations_souhaitees))
        .order_by(models.DevisRequest.envoye_le.desc())
    )
    result = await db.execute(stmt)
    return list(result.scalars().unique().all())


def to_summary(devis: models.DevisRequest) -> schemas.DevisRequestSummary:
    return schemas.DevisRequestSummary(
        id=devis.id,
        reference=devis.reference,
        prenom=devis.prenom,
        nom=devis.nom,
        email=devis.email,
        telephone=devis.telephone,
        pays=devis.pays,
        societe=devis.societe,
        fonction=devis.fonction,
        robot_id=devis.robot_id,
        prestations_souhaitees=[p.niveau for p in devis.prestations_souhaitees],
        demande_speciale=devis.demande_speciale,
        commercial_assigne=devis.commercial_assigne,
        envoye_le=devis.envoye_le,
    )
