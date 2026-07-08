"""
Enums partagés entre domaines — alignés strictement sur
`frontend/src/types/robot.types.ts` et `user.types.ts` pour que le contrat
JSON échangé avec le frontend Vue existant ne nécessite aucune adaptation.
"""
from __future__ import annotations

from enum import Enum


class UserRole(str, Enum):
    COMMERCIAL = "commercial"
    RESPONSABLE_RAN = "responsable_ran"
    # "client" n'est jamais un rôle authentifié côté backend : la vue client
    # est soit anonyme (lien partagé), soit vue via le toggle d'un commercial
    # authentifié (CDC §5.2). Elle n'a donc pas de compte propre.


class RobotType(str, Enum):
    ARTICULE = "Articulé"
    SOUDURE_ARC = "Soudure arc"
    PALETTISATION = "Palettisation"
    PEINTURE = "Peinture"
    DELTA = "Delta"
    COLLABORATIF = "Collaboratif"


class BaieType(str, Enum):
    R_30IB = "R-30iB"
    R_30IB_PLUS = "R-30iB Plus"
    R_30IA = "R-30iA"


class NiveauRenovation(str, Enum):
    PEINTURE = "Peinture"
    STANDARD = "Standard"
    PREMIUM = "Premium"
    QUASI_NEUVE = "Quasi Neuve"
    EXTENSION_GARANTIE = "Extension de garantie"
    ECHANGE_STANDARD = "Échange standard"


class RobotStatut(str, Enum):
    BROUILLON = "Brouillon"
    PUBLIE = "Publié"
    DESACTIVE = "Désactivé"


class AxesCount(int, Enum):
    QUATRE = 4
    CINQ = 5
    SIX = 6
    SEPT = 7


class ImportRowStatus(str, Enum):
    ACCEPTE = "accepte"
    ERREUR = "erreur"
    DOUBLON = "doublon"
