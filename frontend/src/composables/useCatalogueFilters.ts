import { ref, watch } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import { useRobotsStore } from '@/stores/robots.store'
import type { CatalogueFilters } from '@/types'

/**
 * Logique métier du moteur de recherche (CDC §3.1) : debounce sur la
 * saisie texte, application immédiate des autres filtres, refetch via
 * le store. Les composants de filtres restent "dumb" et ne font
 * qu'émettre des intentions vers ce composable.
 */
export function useCatalogueFilters() {
  const store = useRobotsStore()
  const { filters, isLoading, resultCount } = storeToRefs(store)

  const rechercheLocale = ref(filters.value.recherche)

  const debouncedSearch = useDebounceFn((value: string) => {
    store.setFilters({ recherche: value })
    store.fetchRobots()
  }, 300)

  watch(rechercheLocale, (value) => debouncedSearch(value))

  function updateFilter<K extends keyof CatalogueFilters>(key: K, value: CatalogueFilters[K]) {
    store.setFilters({ [key]: value } as Partial<CatalogueFilters>)
    store.fetchRobots()
  }

  function resetAll() {
    rechercheLocale.value = ''
    store.resetFilters()
    store.fetchRobots()
  }

  return { filters, isLoading, resultCount, rechercheLocale, updateFilter, resetAll }
}


