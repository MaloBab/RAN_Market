<script setup lang="ts">
import type { PrestationRenovation } from '@/types'
import BaseBadge from '@/components/ui/BaseBadge.vue'

defineProps<{ prestations: PrestationRenovation[] }>()
</script>

<template>
  <ul class="grid sm:grid-cols-2 gap-2">
    <li v-for="p in prestations" :key="p.niveau" class="flex items-center justify-between bg-ran-graphite-900 border border-ran-graphite-700 px-3 py-2.5">
      <span class="text-sm text-ran-graphite-100">{{ p.niveau }}</span>
      <BaseBadge tone="steel">{{ p.garantieMois ? `${p.garantieMois} mois` : 'à définir' }}</BaseBadge>
    </li>
  </ul>
</template>
