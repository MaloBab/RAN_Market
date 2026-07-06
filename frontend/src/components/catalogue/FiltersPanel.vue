<script setup lang="ts">
import { ref } from 'vue'
import { useCatalogueFilters } from '@/composables/useCatalogueFilters'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import type { RobotType, BaieType } from '@/types'
import { ChevronDown, ChevronUp, RotateCcw, SlidersHorizontal, Search } from 'lucide-vue-next'

const { filters, rechercheLocale, updateFilter, resetAll, resultCount } = useCatalogueFilters()

const TYPES: RobotType[] = ['Articulé', 'Soudure arc', 'Palettisation', 'Peinture', 'Delta', 'Collaboratif']
const BAIES: BaieType[] = ['R-30iB', 'R-30iB Plus', 'R-30iA']
const AXES = [4, 5, 6, 7] as const

const showAdvanced = ref(false)

const chipClass = (active: boolean) =>
  active
    ? 'border-brand-red-600 text-brand-red-600 bg-brand-red-100/60'
    : 'border-ink-200 text-ink-600 hover:border-ink-300 hover:bg-ink-50'

function toggleType(t: RobotType) {
  const current = filters.value.types
  updateFilter('types', current.includes(t) ? current.filter((x) => x !== t) : [...current, t])
}
function toggleAxe(a: 4 | 5 | 6 | 7) {
  const current = filters.value.axes
  updateFilter('axes', current.includes(a) ? current.filter((x) => x !== a) : [...current, a])
}
</script>

<template>
  <BaseCard as="aside" class="p-5 space-y-5 h-fit" aria-label="Filtres du catalogue">
    <div class="flex items-center gap-1.5 text-sm font-semibold text-ink-900">
      <SlidersHorizontal class="size-4 text-ink-400" aria-hidden="true" /> Filtres
    </div>

    <div>
      <label for="filter-search" class="block text-xs font-medium text-ink-500 mb-1.5">Recherche modèle</label>
      <div class="relative">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-ink-400" aria-hidden="true" />
        <BaseInput id="filter-search" v-model="rechercheLocale" placeholder="Ex : ARC Mate, M-710iC…" class="pl-9" />
      </div>
    </div>

    <div role="group" aria-labelledby="filter-type-label">
      <span id="filter-type-label" class="block text-xs font-medium text-ink-500 mb-1.5">Type de robot</span>
      <div class="flex flex-wrap gap-1.5">
        <button
          v-for="t in TYPES" :key="t" @click="toggleType(t)"
          class="px-2.5 min-h-9 rounded-full text-xs font-medium border transition-colors cursor-pointer"
          :class="chipClass(filters.types.includes(t))"
          :aria-pressed="filters.types.includes(t)"
        >{{ t }}</button>
      </div>
    </div>

    <button
      class="flex items-center gap-1.5 text-xs font-semibold text-ink-500 hover:text-ink-900 min-h-9 cursor-pointer"
      :aria-expanded="showAdvanced"
      aria-controls="filters-advanced"
      @click="showAdvanced = !showAdvanced"
    >
      <component :is="showAdvanced ? ChevronUp : ChevronDown" class="size-3.5" aria-hidden="true" />
      {{ showAdvanced ? 'Masquer les filtres avancés' : 'Afficher plus de filtres' }}
    </button>

    <div v-if="showAdvanced" id="filters-advanced" class="space-y-5 border-t border-ink-200 pt-5">
      <div>
        <span id="filter-payload-label" class="block text-xs font-medium text-ink-500 mb-1.5">Payload (kg)</span>
        <div class="grid grid-cols-2 gap-2" role="group" aria-labelledby="filter-payload-label">
          <BaseInput type="number" :model-value="String(filters.payloadKg?.min ?? '')" placeholder="min" @update:modelValue="v => updateFilter('payloadKg', { ...filters.payloadKg, min: v ? Number(v) : undefined })" />
          <BaseInput type="number" :model-value="String(filters.payloadKg?.max ?? '')" placeholder="max" @update:modelValue="v => updateFilter('payloadKg', { ...filters.payloadKg, max: v ? Number(v) : undefined })" />
        </div>
      </div>

      <div>
        <span id="filter-rayon-label" class="block text-xs font-medium text-ink-500 mb-1.5">Rayon d'action (m)</span>
        <div class="grid grid-cols-2 gap-2" role="group" aria-labelledby="filter-rayon-label">
          <BaseInput type="number" :model-value="String(filters.rayonActionM?.min ?? '')" placeholder="min" @update:modelValue="v => updateFilter('rayonActionM', { ...filters.rayonActionM, min: v ? Number(v) : undefined })" />
          <BaseInput type="number" :model-value="String(filters.rayonActionM?.max ?? '')" placeholder="max" @update:modelValue="v => updateFilter('rayonActionM', { ...filters.rayonActionM, max: v ? Number(v) : undefined })" />
        </div>
      </div>

      <div>
        <span id="filter-axes-label" class="block text-xs font-medium text-ink-500 mb-1.5">Nombre d'axes</span>
        <div class="flex gap-1.5" role="group" aria-labelledby="filter-axes-label">
          <button
            v-for="a in AXES" :key="a" @click="toggleAxe(a)"
            class="size-11 rounded-lg text-xs font-medium border transition-colors cursor-pointer"
            :class="chipClass(filters.axes.includes(a))"
            :aria-pressed="filters.axes.includes(a)"
          >{{ a }}</button>
        </div>
      </div>

      <div>
        <label for="filter-baie" class="block text-xs font-medium text-ink-500 mb-1.5">Type de baie</label>
        <BaseSelect id="filter-baie" :model-value="filters.typeBaie ?? ''" :options="BAIES.map(b => ({ value: b, label: b }))" placeholder="Toutes" @update:modelValue="v => updateFilter('typeBaie', (v || undefined) as any)" />
      </div>
    </div>

    <div class="flex items-center justify-between border-t border-ink-200 pt-4">
      <span class="text-xs font-medium text-ink-500" role="status" aria-live="polite">{{ resultCount }} résultat(s)</span>
      <BaseButton variant="ghost" size="sm" @click="resetAll">
        <RotateCcw class="size-3.5" aria-hidden="true" /> Réinitialiser
      </BaseButton>
    </div>
  </BaseCard>
</template>
