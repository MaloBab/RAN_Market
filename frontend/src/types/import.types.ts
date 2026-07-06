/**
 * Import Excel back-office RAN (CDC §3.6).
 */

export type ImportRowStatus = 'accepte' | 'erreur' | 'doublon'

export interface ImportRowResult {
  ligne: number
  idRobot: string
  statut: ImportRowStatus
  message?: string
}

export interface ImportReport {
  totalLignes: number
  accepte: number
  erreurs: number
  doublons: number
  details: ImportRowResult[]
}

export type ImportPhase = 'idle' | 'uploading' | 'parsing' | 'done' | 'failed'


