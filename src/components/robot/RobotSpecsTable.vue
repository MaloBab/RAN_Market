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
  <dl class="grid grid-cols-2 gap-x-6 gap-y-3">
    <div v-for="[label, getter] in rows" :key="label" class="border-b border-ran-graphite-800 pb-2">
      <dt class="text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400">{{ label }}</dt>
      <dd class="text-sm text-ran-graphite-100 mt-0.5">{{ getter(robot) }}</dd>
    </div>
  </dl>
</template>
