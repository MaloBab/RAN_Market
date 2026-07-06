<script setup lang="ts">
import type { Robot } from '@/types'

defineProps<{ robot: Robot }>()
const rows = [
  ['Payload', (r: Robot) => `${r.caracteristiques.payloadKg} kg`],
  ['Rayon d\'action', (r: Robot) => `${(r.caracteristiques.rayonActionMm / 1000).toFixed(2)} m`],
  ['Nombre d\'axes', (r: Robot) => String(r.caracteristiques.axes)],
  ['Type de baie', (r: Robot) => r.caracteristiques.typeBaie],
  ['Protection IP', (r: Robot) => r.caracteristiques.protectionIp],
  ['Montage', (r: Robot) => r.caracteristiques.montage],
  ['Année de mise en service', (r: Robot) => String(r.anneeMiseEnService)],
  ["Heures d'utilisation", (r: Robot) => `${r.heuresUtilisation.toLocaleString('fr-FR')} h`]
] as const
</script>

<template>
  <dl class="grid grid-cols-2 gap-x-6 gap-y-4 bg-white border border-ink-200 rounded-xl p-4">
    <div v-for="[label, getter] in rows" :key="label" class="border-b border-ink-100 pb-2.5">
      <dt class="text-xs font-medium text-ink-500">{{ label }}</dt>
      <dd class="text-sm font-medium text-ink-900 mt-1">{{ getter(robot) }}</dd>
    </div>
  </dl>
</template>
