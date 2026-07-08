"""
Seed de données de démonstration.

Reprend les mêmes comptes que l'ancien mock frontend
(`frontend/src/services/mocks/users.mock.ts`) — mêmes emails et mots de
passe, mais désormais hachés bcrypt et vérifiés côté serveur. Ajoute
également quelques fiches robots publiées pour tester immédiatement le
catalogue sans passer par l'import Excel.

Usage :
    python -m scripts.seed
"""
from __future__ import annotations

import asyncio
import uuid

from sqlalchemy import select #type: ignore

from src.auth.models import User
from src.database import Base, async_session_factory, engine
from src.robots.models import Robot, RobotPrestation
from src.security import hash_password
from src.shared.enums import BaieType, NiveauRenovation, RobotStatut, RobotType, UserRole

DEMO_USERS = [
    dict(
        id="usr-001", nom="Camille Berthier", email="commercial@fanuc-ran.example",
        password="Commercial#2026", role=UserRole.COMMERCIAL,
    ),
    dict(
        id="usr-002", nom="Julien Ferreira", email="responsable@fanuc-ran.example",
        password="ResponsableRAN#2026", role=UserRole.RESPONSABLE_RAN,
    ),
]

DEMO_ROBOTS = [
    dict(
        id="FANUC-2024-001", modele="ARC Mate 100iD", type=RobotType.SOUDURE_ARC, categorie="Soudure arc",
        annee_mise_en_service=2018, heures_utilisation=14500,
        description_courte="Robot de soudure compact, rénové niveau Premium, idéal petites séries.",
        payload_kg=12, rayon_action_mm=1441, axes=6, type_baie=BaieType.R_30IB_PLUS,
        protection_ip="IP54", montage="Sol", prix_catalogue_eur=28000, remise_pct=10,
        quantite_stock=3, nombre_offres_en_cours=1,
        prestations=[NiveauRenovation.STANDARD, NiveauRenovation.PREMIUM],
    ),
    dict(
        id="FANUC-2023-014", modele="M-20iD/25", type=RobotType.ARTICULE, categorie="Manutention",
        annee_mise_en_service=2016, heures_utilisation=21000,
        description_courte="Robot polyvalent 6 axes, forte charge utile, rénovation Quasi Neuve.",
        payload_kg=25, rayon_action_mm=1831, axes=6, type_baie=BaieType.R_30IB,
        protection_ip="IP67", montage="Sol / Suspendu", prix_catalogue_eur=34500, remise_pct=0,
        quantite_stock=1, nombre_offres_en_cours=0,
        prestations=[NiveauRenovation.QUASI_NEUVE, NiveauRenovation.EXTENSION_GARANTIE],
    ),
    dict(
        id="FANUC-2022-007", modele="LR Mate 200iD", type=RobotType.COLLABORATIF, categorie="Collaboratif",
        annee_mise_en_service=2019, heures_utilisation=8200,
        description_courte="Petit robot compact, adapté aux cellules collaboratives et à l'assemblage.",
        payload_kg=7, rayon_action_mm=717, axes=6, type_baie=BaieType.R_30IB_PLUS,
        protection_ip="IP54", montage="Table", prix_catalogue_eur=16800, remise_pct=15,
        quantite_stock=5, nombre_offres_en_cours=2,
        prestations=[NiveauRenovation.PEINTURE, NiveauRenovation.STANDARD],
    ),
]


async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as db:
        for u in DEMO_USERS:
            existing = await db.execute(select(User).where(User.email == u["email"]))
            if existing.scalar_one_or_none() is not None:
                continue
            db.add(
                User(
                    id=u["id"], nom=u["nom"], email=u["email"],
                    hashed_password=hash_password(u["password"]), role=u["role"], is_active=True,
                )
            )

        for r in DEMO_ROBOTS:
            existing = await db.get(Robot, r["id"])
            if existing is not None:
                continue
            prestations = r.pop("prestations")
            robot = Robot(**r, statut=RobotStatut.PUBLIE)
            robot.prestations = [RobotPrestation(niveau=n, garantie_mois=None) for n in prestations]
            db.add(robot)

        await db.commit()

    print("Seed terminé :")
    for u in DEMO_USERS:
        print(f"  - {u['email']} / {u['password']}  (rôle: {u['role'].value})")
        
    await engine.dispose() 


if __name__ == "__main__":
    asyncio.run(seed())
