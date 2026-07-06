<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useRobotsStore } from '@/stores/robots.store'
import { useViewStrategy } from '@/composables/useViewStrategy'
import { formatEUR } from '@/utils/format'
import BaseCard from '@/components/ui/BaseCard.vue'
import { GitCompareArrows } from 'lucide-vue-next'

const store = useRobotsStore()
const { compareRobots } = storeToRefs(store)
const { prixFinal } = useViewStrategy()

const rows = [
  { label: 'Payload', get: (r: any) => `${r.caracteristiques.payloadKg} kg` },
  { label: 'Rayon d\'action', get: (r: any) => `${(r.caracteristiques.rayonActionMm / 1000).toFixed(2)} m` },
  { label: 'Axes', get: (r: any) => r.caracteristiques.axes },
  { label: 'Type de baie', get: (r: any) => r.caracteristiques.typeBaie },
  { label: 'Année', get: (r: any) => r.anneeMiseEnService },
  { label: 'Prix', get: (r: any) => formatEUR(prixFinal(r)), highlight: true }
]

function isDivergent(rowLabel: string) {
  if (compareRobots.value.length < 2) return false
  const row = rows.find((r) => r.label === rowLabel)!
  const values = compareRobots.value.map((r) => row.get(r))
  return new Set(values).size > 1
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
    <h1 class="font-heading font-extrabold text-3xl sm:text-4xl tracking-tight text-ink-900 mb-6">Comparateur</h1>

    <div v-if="compareRobots.length < 2" class="flex flex-col items-center gap-3 text-center text-ink-500 py-20 rounded-xl border border-dashed border-ink-200 bg-white">
      <GitCompareArrows class="size-8 text-ink-300" aria-hidden="true" />
      <p>Sélectionnez deux robots depuis le catalogue pour lancer la comparaison.</p>
    </div>

    <template v-else>
      <p class="text-xs font-medium text-ink-500 mb-3 flex items-center gap-1.5">
        <span class="inline-block size-2 rounded-full bg-brand-yellow-500" aria-hidden="true" /> Ligne surlignée = écart entre les robots
      </p>
      <BaseCard class="overflow-x-auto">
        <table class="w-full text-sm min-w-[420px]">
          <caption class="sr-only">Comparaison technique et tarifaire des robots sélectionnés</caption>
          <thead>
            <tr class="border-b border-ink-200">
              <th scope="col" class="text-left p-3 text-xs font-medium text-ink-500">Critère</th>
              <th v-for="r in compareRobots" :key="r.id" scope="col" class="text-left p-3">
                <p class="font-heading font-semibold text-lg text-ink-900">{{ r.modele }}</p>
                <p class="text-xs text-ink-500 font-mono">{{ r.id }}</p>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in rows" :key="row.label" class="border-b border-ink-100" :class="isDivergent(row.label) && 'bg-brand-yellow-100/50'">
              <th scope="row" class="p-3 text-left text-xs font-medium text-ink-500">{{ row.label }}</th>
              <td v-for="r in compareRobots" :key="r.id" class="p-3" :class="row.highlight ? 'text-ink-900 font-heading font-bold text-lg' : 'text-ink-700'">
                {{ row.get(r) }}
              </td>
            </tr>
          </tbody>
        </table>
      </BaseCard>
    </template>
  </div>
</template>
