from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.robots import models, schemas
from src.robots.filters import CatalogueFilters
from src.shared.enums import RobotStatut
from src.shared.exceptions import ConflictError, NotFoundError

_EAGER_LOAD = (
    selectinload(models.Robot.prestations),
    selectinload(models.Robot.photos_avant),
    selectinload(models.Robot.galerie_avant_apres),
    selectinload(models.Robot.historique_ventes),
)


# ---------------------------------------------------------------------------
# Lecture — catalogue public (CDC §3.1) : uniquement les fiches "Publié"
# ---------------------------------------------------------------------------

async def list_published_robots(db: AsyncSession, filters: CatalogueFilters) -> list[models.Robot]:
    stmt = select(models.Robot).where(models.Robot.statut == RobotStatut.PUBLIE).options(*_EAGER_LOAD)

    if filters.recherche.strip():
        needle = f"%{filters.recherche.strip().lower()}%"
        from sqlalchemy import func, or_

        stmt = stmt.where(
            or_(func.lower(models.Robot.modele).like(needle), func.lower(models.Robot.id).like(needle))
        )
    if filters.types:
        stmt = stmt.where(models.Robot.type.in_(filters.types))
    if filters.axes:
        stmt = stmt.where(models.Robot.axes.in_(filters.axes))
    if filters.type_baie:
        stmt = stmt.where(models.Robot.type_baie == filters.type_baie)
    if filters.payload_kg:
        if filters.payload_kg.min is not None:
            stmt = stmt.where(models.Robot.payload_kg >= filters.payload_kg.min)
        if filters.payload_kg.max is not None:
            stmt = stmt.where(models.Robot.payload_kg <= filters.payload_kg.max)
    if filters.rayon_action_m:
        if filters.rayon_action_m.min is not None:
            stmt = stmt.where(models.Robot.rayon_action_mm >= filters.rayon_action_m.min * 1000)
        if filters.rayon_action_m.max is not None:
            stmt = stmt.where(models.Robot.rayon_action_mm <= filters.rayon_action_m.max * 1000)
    if filters.annee_mise_en_service:
        if filters.annee_mise_en_service.min is not None:
            stmt = stmt.where(models.Robot.annee_mise_en_service >= filters.annee_mise_en_service.min)
        if filters.annee_mise_en_service.max is not None:
            stmt = stmt.where(models.Robot.annee_mise_en_service <= filters.annee_mise_en_service.max)
    if filters.heures_utilisation:
        if filters.heures_utilisation.min is not None:
            stmt = stmt.where(models.Robot.heures_utilisation >= filters.heures_utilisation.min)
        if filters.heures_utilisation.max is not None:
            stmt = stmt.where(models.Robot.heures_utilisation <= filters.heures_utilisation.max)

    stmt = stmt.order_by(models.Robot.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().unique().all())


async def get_published_robot(db: AsyncSession, robot_id: str) -> models.Robot | None:
    stmt = (
        select(models.Robot)
        .where(models.Robot.id == robot_id, models.Robot.statut == RobotStatut.PUBLIE)
        .options(*_EAGER_LOAD)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# ---------------------------------------------------------------------------
# Lecture — back-office RAN (toutes fiches, tous statuts)
# ---------------------------------------------------------------------------

async def list_all_robots(db: AsyncSession) -> list[models.Robot]:
    stmt = select(models.Robot).options(*_EAGER_LOAD).order_by(models.Robot.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().unique().all())


async def get_robot_or_404(db: AsyncSession, robot_id: str) -> models.Robot:
    stmt = select(models.Robot).where(models.Robot.id == robot_id).options(*_EAGER_LOAD)
    result = await db.execute(stmt)
    robot = result.scalar_one_or_none()
    if robot is None:
        raise NotFoundError(f"Fiche robot '{robot_id}' introuvable.")
    return robot


# ---------------------------------------------------------------------------
# Écriture — back-office RAN
# ---------------------------------------------------------------------------

async def create_robot(db: AsyncSession, payload: schemas.RobotCreate) -> models.Robot:
    existing = await db.get(models.Robot, payload.id)
    if existing is not None:
        raise ConflictError(f"Une fiche avec l'ID {payload.id} existe déjà.")

    robot = models.Robot(
        id=payload.id,
        modele=payload.modele,
        type=payload.type,
        categorie=payload.categorie,
        annee_mise_en_service=payload.annee_mise_en_service,
        heures_utilisation=payload.heures_utilisation,
        description_courte=payload.description_courte,
        statut=RobotStatut.BROUILLON,  # Toujours Brouillon à la création (CDC §2.3, §3.6)
        payload_kg=payload.caracteristiques.payload_kg,
        rayon_action_mm=payload.caracteristiques.rayon_action_mm,
        axes=payload.caracteristiques.axes,
        type_baie=payload.caracteristiques.type_baie,
        protection_ip=payload.caracteristiques.protection_ip,
        montage=payload.caracteristiques.montage,
        datasheet_url=payload.documentation.datasheet_url,
        flyer_url=payload.documentation.flyer_url,
        brochure_url=payload.documentation.brochure_url,
        video_url=payload.media.video_url,
        prix_catalogue_eur=payload.prix_catalogue_eur,
        remise_pct=payload.remise_pct,
        quantite_stock=payload.quantite_stock,
        nombre_offres_en_cours=payload.nombre_offres_en_cours,
    )
    robot.prestations = [
        models.RobotPrestation(niveau=p.niveau, garantie_mois=p.garantie_mois)
        for p in payload.prestations_disponibles
    ]
    robot.photos_avant = [
        models.RobotPhoto(url=url, ordre=i) for i, url in enumerate(payload.media.photos_avant)
    ]
    robot.galerie_avant_apres = [
        models.RobotGalerieItem(avant_url=g.avant, apres_url=g.apres, legende=g.legende)
        for g in payload.media.galerie_avant_apres
    ]

    db.add(robot)
    await db.commit()
    return await get_robot_or_404(db, robot.id)


async def update_robot(db: AsyncSession, robot_id: str, payload: schemas.RobotUpdate) -> models.Robot:
    robot = await get_robot_or_404(db, robot_id)

    simple_fields = (
        "modele", "type", "categorie", "annee_mise_en_service", "heures_utilisation",
        "description_courte", "prix_catalogue_eur", "remise_pct", "quantite_stock",
        "nombre_offres_en_cours", "statut",
    )
    for field_name in simple_fields:
        value = getattr(payload, field_name)
        if value is not None:
            setattr(robot, field_name, value)

    if payload.caracteristiques is not None:
        c = payload.caracteristiques
        robot.payload_kg = c.payload_kg
        robot.rayon_action_mm = c.rayon_action_mm
        robot.axes = c.axes
        robot.type_baie = c.type_baie
        robot.protection_ip = c.protection_ip
        robot.montage = c.montage

    if payload.documentation is not None:
        robot.datasheet_url = payload.documentation.datasheet_url
        robot.flyer_url = payload.documentation.flyer_url
        robot.brochure_url = payload.documentation.brochure_url

    if payload.media is not None:
        robot.video_url = payload.media.video_url
        robot.photos_avant = [
            models.RobotPhoto(url=url, ordre=i) for i, url in enumerate(payload.media.photos_avant)
        ]
        robot.galerie_avant_apres = [
            models.RobotGalerieItem(avant_url=g.avant, apres_url=g.apres, legende=g.legende)
            for g in payload.media.galerie_avant_apres
        ]

    if payload.prestations_disponibles is not None:
        robot.prestations = [
            models.RobotPrestation(niveau=p.niveau, garantie_mois=p.garantie_mois)
            for p in payload.prestations_disponibles
        ]

    await db.commit()
    return await get_robot_or_404(db, robot_id)


# ---------------------------------------------------------------------------
# Mapping ORM → schémas de sortie (séparation stricte vue client / commerciale)
# ---------------------------------------------------------------------------

def _map_common(robot: models.Robot) -> dict:
    return {
        "id": robot.id,
        "modele": robot.modele,
        "type": robot.type,
        "categorie": robot.categorie,
        "annee_mise_en_service": robot.annee_mise_en_service,
        "heures_utilisation": robot.heures_utilisation,
        "description_courte": robot.description_courte,
        "caracteristiques": schemas.CaracteristiquesSchema(
            payload_kg=robot.payload_kg,
            rayon_action_mm=robot.rayon_action_mm,
            axes=robot.axes,
            type_baie=robot.type_baie,
            protection_ip=robot.protection_ip,
            montage=robot.montage,
        ),
        "prestations_disponibles": [
            schemas.PrestationSchema(niveau=p.niveau, garantie_mois=p.garantie_mois)
            for p in robot.prestations
        ],
        "media": schemas.MediaSchema(
            photos_avant=[p.url for p in robot.photos_avant],
            galerie_avant_apres=[
                schemas.GalerieItemSchema(avant=g.avant_url, apres=g.apres_url, legende=g.legende)
                for g in robot.galerie_avant_apres
            ],
            video_url=robot.video_url,
        ),
        "documentation": schemas.DocumentationSchema(
            datasheet_url=robot.datasheet_url,
            flyer_url=robot.flyer_url,
            brochure_url=robot.brochure_url,
        ),
    }


def to_client_response(robot: models.Robot) -> schemas.RobotClientResponse:
    """Vue Client : ne construit même pas les champs commerciaux (pas de risque de fuite par oubli)."""
    return schemas.RobotClientResponse(**_map_common(robot))


def to_commercial_response(robot: models.Robot) -> schemas.RobotCommercialResponse:
    """Vue Commerciale : réservée aux appels authentifiés avec rôle commercial/responsable_ran (vérifié dans le router)."""
    prix_final = round(robot.prix_catalogue_eur * (1 - robot.remise_pct / 100), 2)
    return schemas.RobotCommercialResponse(
        **_map_common(robot),
        commercial=schemas.CommercialDataSchema(
            prix_catalogue_eur=robot.prix_catalogue_eur,
            remise_pct=robot.remise_pct,
            quantite_stock=robot.quantite_stock,
            nombre_offres_en_cours=robot.nombre_offres_en_cours,
            historique_ventes=[
                schemas.VenteHistoriqueSchema(periode=v.periode, unites_vendues=v.unites_vendues)
                for v in robot.historique_ventes
            ] or None,
        ),
        statut=robot.statut,
        prix_final_eur=prix_final,
    )
