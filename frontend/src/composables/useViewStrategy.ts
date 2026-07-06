import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import type { Robot } from '@/types'
import { useAuthStore } from '@/stores/auth.store'

/**
 * Pattern Strategy : encapsule les règles "qu'est-ce qui est visible
 * selon la vue active" en un seul endroit, plutôt que de disséminer des
 * `v-if="mode === 'commerciale'"` dans chaque composant. Toute nouvelle
 * vue (ex: future vue "Partenaire") s'ajoute ici sans toucher l'UI.
 */
export interface RobotViewFields {
  showPrix: boolean
  showStock: boolean
  showOffres: boolean
  showHistoriqueVentes: boolean
  showComparateurPrix: boolean
  showComingSoon: boolean
}

const COMMERCIALE_STRATEGY: RobotViewFields = {
  showPrix: true,
  showStock: true,
  showOffres: true,
  showHistoriqueVentes: true,
  showComparateurPrix: true,
  showComingSoon: true
}

const CLIENT_STRATEGY: RobotViewFields = {
  showPrix: false,
  showStock: false,
  showOffres: false,
  showHistoriqueVentes: false,
  showComparateurPrix: false,
  showComingSoon: false
}

export function useViewStrategy() {
  const auth = useAuthStore()
  const { effectiveDisplayMode, canToggleView } = storeToRefs(auth)

  const fields = computed<RobotViewFields>(() =>
    effectiveDisplayMode.value === 'commerciale' ? COMMERCIALE_STRATEGY : CLIENT_STRATEGY
  )

  const isCommerciale = computed(() => effectiveDisplayMode.value === 'commerciale')

  /** Prix final HT à afficher (uniquement pertinent si showPrix). */
  function prixFinal(robot: Robot): number {
    const { prixCatalogueEUR, remisePct } = robot.commercial
    return Math.round(prixCatalogueEUR * (1 - remisePct / 100))
  }

  return { fields, isCommerciale, canToggleView, effectiveDisplayMode, prixFinal, toggle: auth.toggleDisplayMode }
}


