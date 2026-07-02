/**
 * Filtres cumulables du catalogue (CDC §3.1).
 * Toutes les bornes sont inclusives ; `undefined` = filtre inactif.
 */
import type { BaieType, RobotType } from './robot.types'

export interface NumericRange {
  min?: number
  max?: number
}

export interface CatalogueFilters {
  recherche: string // nom / modèle, autocomplétion côté UI
  types: RobotType[]
  payloadKg?: NumericRange
  rayonActionM?: NumericRange
  axes: Array<4 | 5 | 6 | 7>
  typeBaie?: BaieType
  anneeMiseEnService?: NumericRange
  heuresUtilisation?: NumericRange
}

export const EMPTY_FILTERS: CatalogueFilters = {
  recherche: '',
  types: [],
  axes: []
}
