from __future__ import annotations

from fastapi import APIRouter, Depends, Request #type: ignore
from slowapi import Limiter #type: ignore
from slowapi.util import get_remote_address #type: ignore
from sqlalchemy.ext.asyncio import AsyncSession #type: ignore

from src.auth.dependencies import require_roles
from src.auth.models import User
from src.database import get_db
from src.devis import schemas, service
from src.shared.enums import UserRole

router = APIRouter(prefix="/devis", tags=["devis"])
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=schemas.DevisSubmissionResult, status_code=201)
@limiter.limit("10/hour")
async def submit_devis_request(request: Request, payload: schemas.DevisRequestCreate, db: AsyncSession = Depends(get_db)):
    """
    POST /devis — formulaire de demande de devis (CDC §3.5), accessible
    sans authentification (client ou commercial). Limité par IP pour
    prévenir le spam applicatif.
    """
    devis = await service.create_devis_request(db, payload)
    return schemas.DevisSubmissionResult(
        reference=devis.reference,
        commercial_assigne=devis.commercial_assigne,
        envoye_le=devis.envoye_le,
    )


@router.get("", response_model=list[schemas.DevisRequestSummary])
async def list_devis_requests(current_user: User = Depends(require_roles(UserRole.COMMERCIAL, UserRole.RESPONSABLE_RAN)), db: AsyncSession = Depends(get_db)):
    """GET /devis — suivi back-office des demandes reçues, réservé aux comptes authentifiés."""
    devis_list = await service.list_devis_requests(db)
    return [service.to_summary(d) for d in devis_list]
