import type { DevisService } from './api.contracts'
import type { DevisRequest, DevisSubmissionResult } from '@/types'
import { delay } from './delay'

class MockDevisService implements DevisService {
  async submit(payload: DevisRequest): Promise<DevisSubmissionResult> {
    await delay(400)
    if (!payload.email || !payload.nom) {
      throw new Error('Champs obligatoires manquants.')
    }
    return {
      reference: `DEV-${Date.now().toString(36).toUpperCase()}`,
      commercialAssigne: 'M. Lefèvre — Agence Lyon',
      envoyeLe: new Date().toISOString()
    }
  }
}

export const devisService: DevisService = new MockDevisService()
