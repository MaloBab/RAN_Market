import type { ImportService } from './api.contracts'
import type { ImportReport, ImportRowResult } from '@/types'
import { delay } from './delay'

const REQUIRED_COLUMNS = [
  'ID_Robot', 'Modèle', 'Type', 'Payload_kg', 'Rayon_mm', 'Axes',
  'Type_baie', 'Annee_service', 'Heures_utilisation', 'Quantite_stock',
  'Prix_catalogue_EUR', 'Remise_pct', 'Prestations_dispo', 'Description_courte'
]

/**
 * Simule le pipeline `POST /api/back-office/import` du CDC §3.6 :
 * lecture du fichier, "parsing" ligne à ligne avec progression, puis
 * rapport d'import (acceptées / erreurs / doublons).
 */
class MockImportService implements ImportService {
  async importExcel(file: File, onProgress?: (pct: number) => void): Promise<ImportReport> {
    if (!/\.(xlsx|xls)$/i.test(file.name)) {
      throw new Error('Format de fichier invalide. Utilisez le modèle .xlsx fourni.')
    }

    // Nombre de lignes simulé à partir de la taille du fichier (mock only).
    const totalLignes = Math.max(8, Math.min(60, Math.round(file.size / 512)))
    const details: ImportRowResult[] = []

    for (let i = 1; i <= totalLignes; i++) {
      await delay(25)
      onProgress?.(Math.round((i / totalLignes) * 100))

      const roll = Math.random()
      if (roll < 0.08) {
        details.push({
          ligne: i,
          idRobot: `FANUC-IMP-${String(i).padStart(3, '0')}`,
          statut: 'erreur',
          message: `Colonne manquante ou invalide (attendu parmi : ${REQUIRED_COLUMNS[i % REQUIRED_COLUMNS.length]})`
        })
      } else if (roll < 0.14) {
        details.push({
          ligne: i,
          idRobot: `FANUC-IMP-${String(i).padStart(3, '0')}`,
          statut: 'doublon',
          message: 'ID_Robot déjà existant dans le catalogue.'
        })
      } else {
        details.push({
          ligne: i,
          idRobot: `FANUC-IMP-${String(i).padStart(3, '0')}`,
          statut: 'accepte'
        })
      }
    }

    return {
      totalLignes,
      accepte: details.filter((d) => d.statut === 'accepte').length,
      erreurs: details.filter((d) => d.statut === 'erreur').length,
      doublons: details.filter((d) => d.statut === 'doublon').length,
      details
    }
  }
}

export const importService: ImportService = new MockImportService()
