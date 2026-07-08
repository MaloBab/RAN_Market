import type { DevisService } from './api.contracts'
import type { DevisRequest, DevisSubmissionResult } from '@/types'
import { apiFetch } from './http'

class HttpDevisService implements DevisService {
  async submit(payload: DevisRequest): Promise<DevisSubmissionResult> {
    // Les noms de champs (prenom, nom, robotId, prestationsSouhaitees,
    // demandeSpeciale...) matchent déjà l'alias camelCase généré côté
    // backend (DevisRequestCreate) — aucune traduction nécessaire ici.
    return apiFetch<DevisSubmissionResult>('/devis', {
      method: 'POST',
      body: payload
    })
  }
}

export const devisService: DevisService = new HttpDevisService()