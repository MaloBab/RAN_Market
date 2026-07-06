import type { NiveauRenovation } from './robot.types'

export interface DevisRequest {
  prenom: string
  nom: string
  email: string
  telephone: string
  pays: string
  societe?: string
  fonction?: string
  robotId?: string // pré-rempli si accès depuis une fiche
  prestationsSouhaitees: NiveauRenovation[]
  demandeSpeciale?: string
}

export interface DevisSubmissionResult {
  reference: string
  commercialAssigne: string
  envoyeLe: string
}


