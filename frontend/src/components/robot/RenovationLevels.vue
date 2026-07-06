<script setup lang="ts">
import type { PrestationRenovation } from '@/types'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import { ShieldCheck } from 'lucide-vue-next'

defineProps<{ prestations: PrestationRenovation[] }>()
</script>

<template>
  <ul v-if="prestations.length" class="grid sm:grid-cols-2 gap-2">
    <li
      v-for="p in prestations" :key="p.niveau"
      class="flex items-center justify-between gap-3 bg-white border border-ink-200 rounded-xl hover:border-ink-300 transition-colors px-3.5 min-h-11 py-2"
    >
      <span class="flex items-center gap-2 text-sm font-medium text-ink-900">
        <ShieldCheck class="size-4 text-ok-600 shrink-0" aria-hidden="true" />
        {{ p.niveau }}
      </span>
      <BaseBadge tone="neutral">{{ p.garantieMois ? `${p.garantieMois} mois` : 'à définir' }}</BaseBadge>
    </li>
  </ul>
  <p v-else class="text-sm text-ink-500">Aucune prestation de rénovation renseignée pour cette fiche.</p>
</template>
