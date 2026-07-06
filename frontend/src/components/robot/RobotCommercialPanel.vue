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
  <div class="space-y-4 bg-brand-yellow-100/60 border border-brand-yellow-500/40 rounded-xl p-4">
    <div class="flex items-baseline justify-between gap-3 flex-wrap">
      <div>
        <p class="font-heading font-extrabold text-3xl text-ink-900 leading-none">{{ formatEUR(prixFinal) }}</p>
        <p class="text-xs text-ink-500 font-mono mt-1.5">
          Prix catalogue {{ formatEUR(robot.commercial.prixCatalogueEUR) }} · remise {{ robot.commercial.remisePct }}%
        </p>
      </div>
      <BaseBadge :tone="robot.commercial.quantiteStock > 0 ? 'ok' : 'alert'">
        {{ robot.commercial.quantiteStock > 0 ? `${robot.commercial.quantiteStock} en stock` : 'Épuisé' }}
      </BaseBadge>
    </div>

    <div class="flex items-center justify-between text-sm border-t border-brand-yellow-500/30 pt-3">
      <span class="text-ink-500">Offres en cours sur ce robot</span>
      <span class="font-mono font-medium text-ink-900">{{ robot.commercial.nombreOffresEnCours }}</span>
    </div>

    <div v-if="robot.commercial.historiqueVentes?.length" class="border-t border-brand-yellow-500/30 pt-3">
      <p class="text-xs font-medium text-ink-500 mb-2">Historique de ventes</p>
      <div class="flex gap-3">
        <div v-for="h in robot.commercial.historiqueVentes" :key="h.periode" class="flex-1 text-center">
          <p class="font-heading font-bold text-lg text-ink-900">{{ h.unitesVendues }}</p>
          <p class="text-[10px] text-ink-500 font-mono">{{ h.periode }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
