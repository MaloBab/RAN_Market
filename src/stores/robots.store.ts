import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { CatalogueFilters, ComingSoonEntry, Robot } from '@/types'
import { EMPTY_FILTERS } from '@/types'
import { robotService } from '@/services'

export const useRobotsStore = defineStore('robots', () => {
  const robots = ref<Robot[]>([])
  const comingSoon = ref<ComingSoonEntry[]>([])
  const filters = ref<CatalogueFilters>({ ...EMPTY_FILTERS })
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  /** Sélection courante pour le comparateur (max 2, CDC §3.4). */
  const compareIds = ref<string[]>([])

  const resultCount = computed(() => robots.value.length)
  const compareRobots = computed(() =>
    compareIds.value.map((id) => robots.value.find((r) => r.id === id)).filter(Boolean) as Robot[]
  )

  async function fetchRobots() {
    isLoading.value = true
    error.value = null
    try {
      robots.value = await robotService.list(filters.value)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Erreur de chargement du catalogue.'
    } finally {
      isLoading.value = false
    }
  }

  async function fetchComingSoon() {
    comingSoon.value = await robotService.listComingSoon()
  }

  function setFilters(next: Partial<CatalogueFilters>) {
    filters.value = { ...filters.value, ...next }
  }

  function resetFilters() {
    filters.value = { ...EMPTY_FILTERS }
  }

  function toggleCompare(id: string) {
    if (compareIds.value.includes(id)) {
      compareIds.value = compareIds.value.filter((c) => c !== id)
      return
    }
    if (compareIds.value.length >= 2) {
      compareIds.value = [compareIds.value[1] as string, id]
      return
    }
    compareIds.value = [...compareIds.value, id]
  }

  return {
    robots, comingSoon, filters, isLoading, error, compareIds,
    resultCount, compareRobots,
    fetchRobots, fetchComingSoon, setFilters, resetFilters, toggleCompare
  }
})
