<script setup lang="ts">
/**
 * Composant "dumb" : reçoit un Robot + s'appuie sur useViewStrategy pour
 * savoir quoi montrer. Ne connaît jamais directement le rôle utilisateur.
 */
import { RouterLink } from 'vue-router'
import type { Robot } from '@/types'
import { useViewStrategy } from '@/composables/useViewStrategy'
import { useRobotsStore } from '@/stores/robots.store'
import { formatEUR, formatHeures } from '@/utils/format'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import RedactedField from '@/components/ui/RedactedField.vue'
import { Scale, Ruler, GitCompareArrows } from 'lucide-vue-next'

const props = defineProps<{ robot: Robot }>()
const { fields, prixFinal } = useViewStrategy()
const store = useRobotsStore()

const isSelected = () => store.compareIds.includes(props.robot.id)
</script>

<template>
  <BaseCard interactive class="group flex flex-col overflow-hidden">
    <RouterLink :to="`/robot/${robot.id}`" class="block relative aspect-[4/3] overflow-hidden bg-ink-100 rounded-t-xl">
      <img :src="robot.media.photosAvant[0]" :alt="robot.modele" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
      <div class="absolute top-3 left-3 flex gap-1.5">
        <BaseBadge tone="yellow">{{ robot.type }}</BaseBadge>
      </div>
      <div v-if="fields.showStock" class="absolute top-3 right-3">
        <BaseBadge :tone="robot.commercial.quantiteStock > 0 ? 'ok' : 'alert'">
          {{ robot.commercial.quantiteStock > 0 ? `${robot.commercial.quantiteStock} en stock` : 'Épuisé' }}
        </BaseBadge>
      </div>
    </RouterLink>

    <div class="flex flex-col flex-1 p-4 gap-3">
      <div>
        <h3 class="font-heading font-semibold text-lg text-ink-900">{{ robot.modele }}</h3>
        <p class="text-xs text-ink-500 font-mono">{{ robot.id }} · {{ robot.anneeMiseEnService }}</p>
      </div>

      <p class="text-sm text-ink-500 line-clamp-2">{{ robot.descriptionCourte }}</p>

      <div class="flex items-center gap-4 text-xs text-ink-500 font-mono">
        <span class="flex items-center gap-1"><Scale class="size-3.5" aria-hidden="true" />{{ robot.caracteristiques.payloadKg }} kg</span>
        <span class="flex items-center gap-1"><Ruler class="size-3.5" aria-hidden="true" />{{ (robot.caracteristiques.rayonActionMm / 1000).toFixed(2) }} m</span>
        <span>{{ formatHeures(robot.heuresUtilisation) }}</span>
      </div>

      <div class="mt-auto pt-3 border-t border-ink-200 flex items-end justify-between">
        <div>
          <RedactedField :visible="fields.showPrix" width="5.5rem">
            <span class="font-heading font-bold text-xl text-ink-900">{{ formatEUR(prixFinal(robot)) }}</span>
          </RedactedField>
          <p v-if="fields.showPrix && robot.commercial.remisePct > 0" class="text-[11px] text-ink-500 font-mono">
            –{{ robot.commercial.remisePct }}% sur {{ formatEUR(robot.commercial.prixCatalogueEUR) }}
          </p>
        </div>

        <button
          v-if="fields.showComparateurPrix"
          @click="store.toggleCompare(robot.id)"
          class="p-2.5 min-h-11 min-w-11 flex items-center justify-center rounded-lg border transition-colors cursor-pointer"
          :class="isSelected() ? 'border-brand-red-600 text-brand-red-600 bg-brand-red-100/60' : 'border-ink-200 text-ink-400 hover:border-ink-300 hover:text-ink-900 hover:bg-ink-50'"
          :aria-pressed="isSelected()"
          :aria-label="isSelected() ? `Retirer ${robot.modele} du comparateur` : `Ajouter ${robot.modele} au comparateur`"
          :title="isSelected() ? 'Retirer du comparateur' : 'Ajouter au comparateur'"
        >
          <GitCompareArrows class="size-4" aria-hidden="true" />
        </button>
      </div>

      <RouterLink :to="`/robot/${robot.id}`">
        <BaseButton variant="secondary" size="sm" class="w-full">Voir la fiche</BaseButton>
      </RouterLink>
    </div>
  </BaseCard>
</template>
