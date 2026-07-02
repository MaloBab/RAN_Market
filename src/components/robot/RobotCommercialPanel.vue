<script setup lang="ts">
/**
 * Bloc "prix / stock / offres / historique" — n'est monté que si
 * fields.showPrix est vrai (voir RobotDetailView). Isolé dans son
 * propre composant pour que rien de sensible ne soit même présent dans
 * le DOM en Vue Client (pas seulement masqué en CSS — cf. §8.2).
 */
import type { Robot } from '@/types'
import { formatEUR } from '@/utils/format'
import BaseBadge from '@/components/ui/BaseBadge.vue'

defineProps<{ robot: Robot; prixFinal: number }>()
</script>

<template>
  <div class="space-y-4 bg-ran-graphite-900 border border-ran-graphite-700 p-4">
    <div class="flex items-baseline justify-between">
      <div>
        <p class="font-display text-3xl text-ran-yellow-500">{{ formatEUR(prixFinal) }}</p>
        <p class="text-xs text-ran-graphite-400 font-mono">
          Prix catalogue {{ formatEUR(robot.commercial.prixCatalogueEUR) }} · remise {{ robot.commercial.remisePct }}%
        </p>
      </div>
      <BaseBadge :tone="robot.commercial.quantiteStock > 0 ? 'ok' : 'alert'">
        {{ robot.commercial.quantiteStock }} en stock
      </BaseBadge>
    </div>

    <div class="flex items-center justify-between text-sm border-t border-ran-graphite-700 pt-3">
      <span class="text-ran-graphite-400">Offres en cours sur ce robot</span>
      <span class="font-mono text-ran-graphite-100">{{ robot.commercial.nombreOffresEnCours }}</span>
    </div>

    <div v-if="robot.commercial.historiqueVentes?.length" class="border-t border-ran-graphite-700 pt-3">
      <p class="text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-2">Historique de ventes</p>
      <div class="flex gap-3">
        <div v-for="h in robot.commercial.historiqueVentes" :key="h.periode" class="flex-1 text-center">
          <p class="font-display text-lg text-ran-graphite-100">{{ h.unitesVendues }}</p>
          <p class="text-[10px] text-ran-graphite-500 font-mono">{{ h.periode }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
