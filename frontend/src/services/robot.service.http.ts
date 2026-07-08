import type { RobotService } from './api.contracts'
import type { CatalogueFilters, ComingSoonEntry, Robot } from '@/types'
import { apiFetch, ApiError } from './http'

/**
 * Traduit les filtres frontend (camelCase, ranges imbriqués) vers les query
 * params attendus par GET /robots (voir backend/src/robots/router.py).
 */
function buildQueryParams(filters: Partial<CatalogueFilters>): URLSearchParams {
  const params = new URLSearchParams()

  if (filters.recherche) params.set('recherche', filters.recherche)
  for (const type of filters.types ?? []) params.append('types', type)
  for (const axes of filters.axes ?? []) params.append('axes', String(axes))
  if (filters.typeBaie) params.set('type_baie', filters.typeBaie)

  if (filters.payloadKg?.min != null) params.set('payload_kg_min', String(filters.payloadKg.min))
  if (filters.payloadKg?.max != null) params.set('payload_kg_max', String(filters.payloadKg.max))

  if (filters.rayonActionM?.min != null) params.set('rayon_action_m_min', String(filters.rayonActionM.min))
  if (filters.rayonActionM?.max != null) params.set('rayon_action_m_max', String(filters.rayonActionM.max))

  if (filters.anneeMiseEnService?.min != null) params.set('annee_min', String(filters.anneeMiseEnService.min))
  if (filters.anneeMiseEnService?.max != null) params.set('annee_max', String(filters.anneeMiseEnService.max))

  if (filters.heuresUtilisation?.min != null) params.set('heures_min', String(filters.heuresUtilisation.min))
  if (filters.heuresUtilisation?.max != null) params.set('heures_max', String(filters.heuresUtilisation.max))

  return params
}

/**
 * Le payload de création frontend (`Omit<Robot, 'statut'>`) garde les
 * données commerciales sous `commercial: {...}` (aligné sur l'affichage),
 * mais le backend (`RobotCreate`) attend ces mêmes champs à plat. On les
 * "déplie" ici, à la frontière HTTP — aucun composant n'a besoin de le
 * savoir.
 */
function toCreatePayload(input: Omit<Robot, 'statut'>) {
  const { commercial, ...rest } = input
  return {
    ...rest,
    prixCatalogueEUR: commercial!.prixCatalogueEUR,
    remisePct: commercial!.remisePct,
    quantiteStock: commercial!.quantiteStock,
    nombreOffresEnCours: commercial!.nombreOffresEnCours
  }
}

class HttpRobotService implements RobotService {
  async list(filters: Partial<CatalogueFilters>): Promise<Robot[]> {
    const query = buildQueryParams(filters).toString()
    return apiFetch<Robot[]>(`/robots${query ? `?${query}` : ''}`)
  }

  async getById(id: string): Promise<Robot | null> {
    try {
      return await apiFetch<Robot>(`/robots/${encodeURIComponent(id)}`)
    } catch (error) {
      if (error instanceof ApiError && error.status === 404) return null
      throw error
    }
  }

  async listComingSoon(): Promise<ComingSoonEntry[]> {
    return apiFetch<ComingSoonEntry[]>('/coming-soon')
  }

  async create(input: Omit<Robot, 'statut'>): Promise<Robot> {
    return apiFetch<Robot>('/robots', {
      method: 'POST',
      body: toCreatePayload(input)
    })
  }
}

export const robotService: RobotService = new HttpRobotService()