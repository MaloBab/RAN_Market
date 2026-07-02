<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useRobotsStore } from '@/stores/robots.store'
import { useViewStrategy } from '@/composables/useViewStrategy'
import { formatEUR } from '@/utils/format'
import BaseCard from '@/components/ui/BaseCard.vue'

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
  <div class="max-w-4xl mx-auto px-6 py-8">
    <h1 class="font-display text-4xl tracking-wide text-ran-graphite-100 mb-6">Comparateur</h1>

    <div v-if="compareRobots.length < 2" class="text-ran-graphite-400 py-16 text-center">
      Sélectionnez deux robots depuis le catalogue pour lancer la comparaison.
    </div>

    <BaseCard v-else class="overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-ran-graphite-700">
            <th class="text-left p-3 font-mono text-[11px] uppercase text-ran-graphite-400">Critère</th>
            <th v-for="r in compareRobots" :key="r.id" class="text-left p-3">
              <p class="font-display text-lg text-ran-graphite-100">{{ r.modele }}</p>
              <p class="text-[11px] font-mono text-ran-graphite-500">{{ r.id }}</p>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row.label" class="border-b border-ran-graphite-800" :class="isDivergent(row.label) && 'bg-ran-yellow-500/5'">
            <td class="p-3 font-mono text-xs text-ran-graphite-400">{{ row.label }}</td>
            <td v-for="r in compareRobots" :key="r.id" class="p-3" :class="row.highlight && 'text-ran-yellow-500 font-display text-lg'">
              {{ row.get(r) }}
            </td>
          </tr>
        </tbody>
      </table>
    </BaseCard>
  </div>
</template>
