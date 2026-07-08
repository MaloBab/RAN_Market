from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile #type: ignore
from sqlalchemy.ext.asyncio import AsyncSession #type: ignore

from src.auth.dependencies import require_roles
from src.auth.models import User
from src.database import get_db
from src.imports import schemas, service
from src.shared.enums import UserRole

router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("/robots", response_model=schemas.ImportReport)
async def import_robots_excel(file: UploadFile = File(...), current_user: User = Depends(require_roles(UserRole.RESPONSABLE_RAN)), db: AsyncSession = Depends(get_db)):
    """
    POST /imports/robots — import Excel de masse (CDC §3.6), réservé au
    responsable RAN. Toutes les fiches créées sont en statut "Brouillon"
    et nécessitent une validation manuelle avant publication.
    """
    return await service.process_import(db, file, operator_id=current_user.id)
