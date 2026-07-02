/**
 * Domaine "Robot" — structures alignées sur le CDC §3.1, §3.2, §3.6.
 */

export type RobotType =
  | 'Articulé'
  | 'Soudure arc'
  | 'Palettisation'
  | 'Peinture'
  | 'Delta'
  | 'Collaboratif'

export type BaieType = 'R-30iB' | 'R-30iB Plus' | 'R-30iA'

export type NiveauRenovation =
  | 'Peinture'
  | 'Standard'
  | 'Premium'
  | 'Quasi Neuve'
  | 'Extension de garantie'
  | 'Échange standard'

export interface PrestationRenovation {
  niveau: NiveauRenovation
  garantieMois: number | null // null = "à définir"
}

export type RobotStatut = 'Brouillon' | 'Publié' | 'Désactivé'

/** Caractéristiques techniques — communes aux deux vues (commerciale/client). */
export interface RobotCaracteristiques {
  payloadKg: number
  rayonActionMm: number
  axes: 4 | 5 | 6 | 7
  typeBaie: BaieType
  protectionIp: string
  montage: string
}

/** Données strictement internes — jamais exposées en Vue Client. */
export interface RobotDonneesCommerciales {
  prixCatalogueEUR: number
  remisePct: number
  quantiteStock: number
  nombreOffresEnCours: number
  historiqueVentes?: { periode: string; unitesVendues: number }[]
}

export interface RobotMedia {
  photosAvant: string[]
  galerieAvantApres: { avant: string; apres: string; legende?: string }[]
  videoUrl?: string
}

export interface RobotDocumentation {
  datasheetUrl?: string
  flyerUrl?: string
  brochureUrl?: string
}

export interface Robot {
  id: string // ID_Robot, ex: FANUC-2024-001
  modele: string
  type: RobotType
  categorie: string
  anneeMiseEnService: number
  heuresUtilisation: number
  descriptionCourte: string
  caracteristiques: RobotCaracteristiques
  prestationsDisponibles: PrestationRenovation[]
  media: RobotMedia
  documentation: RobotDocumentation
  commercial: RobotDonneesCommerciales
  statut: RobotStatut
}

/** Entrée simplifiée de la section "Coming Soon" (§3.7) — vue commerciale uniquement. */
export interface ComingSoonEntry {
  id: string
  modele: string
  type: RobotType
  disponibiliteEstimee: string // ex: "T1 2027"
  niveauRenovationPrevu: NiveauRenovation
}
