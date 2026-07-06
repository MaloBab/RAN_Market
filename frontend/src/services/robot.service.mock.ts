import type { RobotService } from './api.contracts'
import type { CatalogueFilters, Robot } from '@/types'
import { MOCK_ROBOTS, MOCK_COMING_SOON } from './mocks/robots.mock'
import { delay } from './delay'

/**
 * Implémentation mock de RobotService. Le filtrage reproduit ce qu'on
 * attend d'un futur `GET /api/robots?type=...&payloadMin=...` : c'est
 * volontairement fait ici (et pas dans le composable) pour que le
 * composable n'ait jamais à connaître la forme des données brutes.
 */
class MockRobotService implements RobotService {
  async list(filters: Partial<CatalogueFilters>): Promise<Robot[]> {
    await delay()
    return MOCK_ROBOTS.filter((robot) => this.matches(robot, filters)).map((r) => ({ ...r }))
  }

  async getById(id: string): Promise<Robot | null> {
    await delay(180)
    return MOCK_ROBOTS.find((r) => r.id === id) ?? null
  }

  async listComingSoon() {
    await delay(150)
    return [...MOCK_COMING_SOON]
  }

  async create(input: Omit<Robot, 'statut'>): Promise<Robot> {
    await delay(350)
    if (MOCK_ROBOTS.some((r) => r.id === input.id)) {
      throw new Error(`Une fiche avec l'ID ${input.id} existe déjà.`)
    }
    const created: Robot = { ...input, statut: 'Brouillon' }
    MOCK_ROBOTS.push(created)
    return created
  }

  private matches(robot: Robot, f: Partial<CatalogueFilters>): boolean {
    if (robot.statut !== 'Publié') return false

    if (f.recherche?.trim()) {
      const needle = f.recherche.trim().toLowerCase()
      if (!robot.modele.toLowerCase().includes(needle) && !robot.id.toLowerCase().includes(needle)) {
        return false
      }
    }
    if (f.types?.length && !f.types.includes(robot.type)) return false
    if (f.axes?.length && !f.axes.includes(robot.caracteristiques.axes)) return false
    if (f.typeBaie && robot.caracteristiques.typeBaie !== f.typeBaie) return false

    if (f.payloadKg) {
      const { min, max } = f.payloadKg
      if (min !== undefined && robot.caracteristiques.payloadKg < min) return false
      if (max !== undefined && robot.caracteristiques.payloadKg > max) return false
    }
    if (f.rayonActionM) {
      const rayonM = robot.caracteristiques.rayonActionMm / 1000
      const { min, max } = f.rayonActionM
      if (min !== undefined && rayonM < min) return false
      if (max !== undefined && rayonM > max) return false
    }
    if (f.anneeMiseEnService) {
      const { min, max } = f.anneeMiseEnService
      if (min !== undefined && robot.anneeMiseEnService < min) return false
      if (max !== undefined && robot.anneeMiseEnService > max) return false
    }
    if (f.heuresUtilisation) {
      const { min, max } = f.heuresUtilisation
      if (min !== undefined && robot.heuresUtilisation < min) return false
      if (max !== undefined && robot.heuresUtilisation > max) return false
    }
    return true
  }
}

export const robotService: RobotService = new MockRobotService()


