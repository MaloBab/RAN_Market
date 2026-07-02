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
  <BaseCard bracket class="group flex flex-col overflow-hidden hover:border-ran-steel-500 transition-colors">
    <RouterLink :to="`/robot/${robot.id}`" class="block relative aspect-[4/3] overflow-hidden bg-ran-graphite-800">
      <img :src="robot.media.photosAvant[0]" :alt="robot.modele" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
      <div class="absolute top-2 left-2 flex gap-1.5">
        <BaseBadge tone="yellow">{{ robot.type }}</BaseBadge>
      </div>
      <div v-if="fields.showStock" class="absolute top-2 right-2">
        <BaseBadge :tone="robot.commercial.quantiteStock > 0 ? 'ok' : 'alert'">
          {{ robot.commercial.quantiteStock > 0 ? `${robot.commercial.quantiteStock} en stock` : 'Épuisé' }}
        </BaseBadge>
      </div>
    </RouterLink>

    <div class="flex flex-col flex-1 p-4 gap-3">
      <div>
        <h3 class="font-display text-lg tracking-wide text-ran-graphite-100">{{ robot.modele }}</h3>
        <p class="text-xs text-ran-graphite-400 font-mono">{{ robot.id }} · {{ robot.anneeMiseEnService }}</p>
      </div>

      <p class="text-sm text-ran-graphite-300 line-clamp-2">{{ robot.descriptionCourte }}</p>

      <div class="flex items-center gap-4 text-xs text-ran-graphite-400 font-mono">
        <span class="flex items-center gap-1"><Scale class="size-3.5" />{{ robot.caracteristiques.payloadKg }} kg</span>
        <span class="flex items-center gap-1"><Ruler class="size-3.5" />{{ (robot.caracteristiques.rayonActionMm / 1000).toFixed(2) }} m</span>
        <span>{{ formatHeures(robot.heuresUtilisation) }}</span>
      </div>

      <div class="mt-auto pt-3 border-t border-ran-graphite-700 flex items-end justify-between">
        <div>
          <RedactedField :visible="fields.showPrix" width="5.5rem">
            <span class="font-display text-xl text-ran-yellow-500">{{ formatEUR(prixFinal(robot)) }}</span>
          </RedactedField>
          <p v-if="fields.showPrix && robot.commercial.remisePct > 0" class="text-[11px] text-ran-graphite-400 font-mono">
            –{{ robot.commercial.remisePct }}% sur {{ formatEUR(robot.commercial.prixCatalogueEUR) }}
          </p>
        </div>

        <button
          v-if="fields.showComparateurPrix"
          @click="store.toggleCompare(robot.id)"
          class="p-2 border transition-colors"
          :class="isSelected() ? 'border-ran-yellow-500 text-ran-yellow-500' : 'border-ran-graphite-600 text-ran-graphite-400 hover:border-ran-steel-500'"
          :aria-pressed="isSelected()"
          title="Ajouter au comparateur"
        >
          <GitCompareArrows class="size-4" />
        </button>
      </div>

      <RouterLink :to="`/robot/${robot.id}`">
        <BaseButton variant="secondary" size="sm" class="w-full">Voir la fiche</BaseButton>
      </RouterLink>
    </div>
  </BaseCard>
</template>
