from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user_optional, require_roles
from src.auth.models import User
from src.database import get_db
from src.robots import schemas, service
from src.robots.filters import CatalogueFilters, NumericRange
from src.shared.enums import BaieType, RobotType, UserRole
from src.shared.exceptions import ForbiddenError, NotFoundError

router = APIRouter(prefix="/robots", tags=["robots"])


def _is_commercial_view(user: User | None) -> bool:
    """
    Détermine la vue à servir. Un utilisateur authentifié commercial ou
    responsable_ran reçoit la vue commerciale complète (avec toggle possible
    côté frontend, CDC §5.2) ; tout le reste (anonyme, ou tout autre cas)
    reçoit la vue client strictement filtrée côté serveur.
    """
    return user is not None and user.role in (UserRole.COMMERCIAL, UserRole.RESPONSABLE_RAN)


@router.get("", response_model=list[schemas.RobotCommercialResponse] | list[schemas.RobotClientResponse])
async def list_robots(
    recherche: str = "",
    types: list[RobotType] = Query(default_factory=list),
    axes: list[int] = Query(default_factory=list),
    type_baie: BaieType | None = None,
    payload_kg_min: float | None = None,
    payload_kg_max: float | None = None,
    rayon_action_m_min: float | None = None,
    rayon_action_m_max: float | None = None,
    annee_min: int | None = None,
    annee_max: int | None = None,
    heures_min: int | None = None,
    heures_max: int | None = None,
    current_user: User | None = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    """
    GET /robots — catalogue (CDC §3.1). Seules les fiches au statut
    "Publié" sont jamais renvoyées ici, quel que soit le rôle : le
    back-office dispose de sa propre route pour voir les brouillons.
    """
    filters = CatalogueFilters(
        recherche=recherche,
        types=types,
        axes=axes,
        type_baie=type_baie,
        payload_kg=NumericRange(payload_kg_min, payload_kg_max) if (payload_kg_min or payload_kg_max) else None,
        rayon_action_m=(
            NumericRange(rayon_action_m_min, rayon_action_m_max)
            if (rayon_action_m_min or rayon_action_m_max)
            else None
        ),
        annee_mise_en_service=NumericRange(annee_min, annee_max) if (annee_min or annee_max) else None,
        heures_utilisation=NumericRange(heures_min, heures_max) if (heures_min or heures_max) else None,
    )
    robots = await service.list_published_robots(db, filters)

    if _is_commercial_view(current_user):
        return [service.to_commercial_response(r) for r in robots]
    return [service.to_client_response(r) for r in robots]


@router.get("/compare", response_model=list[schemas.RobotCommercialResponse])
async def compare_robots(
    ids: list[str] = Query(..., min_length=2, max_length=4),
    current_user: User = Depends(require_roles(UserRole.COMMERCIAL, UserRole.RESPONSABLE_RAN)),
    db: AsyncSession = Depends(get_db),
):
    """
    GET /robots/compare — comparateur (CDC §3.4), disponible en vue
    commerciale uniquement (jamais de prix affiché à un client anonyme).
    """
    robots = []
    for robot_id in ids:
        robot = await service.get_published_robot(db, robot_id)
        if robot is None:
            raise NotFoundError(f"Fiche robot '{robot_id}' introuvable ou non publiée.")
        robots.append(robot)
    return [service.to_commercial_response(r) for r in robots]


@router.get(
    "/backoffice/all",
    response_model=list[schemas.RobotCommercialResponse],
)
async def list_all_robots_backoffice(
    current_user: User = Depends(require_roles(UserRole.RESPONSABLE_RAN)),
    db: AsyncSession = Depends(get_db),
):
    """GET /robots/backoffice/all — toutes les fiches, tous statuts (Brouillon/Publié/Désactivé)."""
    robots = await service.list_all_robots(db)
    return [service.to_commercial_response(r) for r in robots]


@router.get("/{robot_id}", response_model=schemas.RobotCommercialResponse | schemas.RobotClientResponse)
async def get_robot(
    robot_id: str,
    current_user: User | None = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
):
    """GET /robots/{id} — fiche détaillée (CDC §3.2/§3.3), publiée uniquement."""
    robot = await service.get_published_robot(db, robot_id)
    if robot is None:
        raise NotFoundError(f"Fiche robot '{robot_id}' introuvable.")

    if _is_commercial_view(current_user):
        return service.to_commercial_response(robot)
    return service.to_client_response(robot)


@router.post("", response_model=schemas.RobotCommercialResponse, status_code=201)
async def create_robot(
    payload: schemas.RobotCreate,
    current_user: User = Depends(require_roles(UserRole.RESPONSABLE_RAN)),
    db: AsyncSession = Depends(get_db),
):
    """POST /robots — création d'une fiche (CDC §3.6), réservé au responsable RAN, statut Brouillon forcé."""
    robot = await service.create_robot(db, payload)
    return service.to_commercial_response(robot)


@router.patch("/{robot_id}", response_model=schemas.RobotCommercialResponse)
async def update_robot(
    robot_id: str,
    payload: schemas.RobotUpdate,
    current_user: User = Depends(require_roles(UserRole.RESPONSABLE_RAN)),
    db: AsyncSession = Depends(get_db),
):
    """PATCH /robots/{id} — mise à jour partielle (stock, statut, tarifs, média...), réservé au responsable RAN."""
    robot = await service.update_robot(db, robot_id, payload)
    return service.to_commercial_response(robot)
