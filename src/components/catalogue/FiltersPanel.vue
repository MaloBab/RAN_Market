<script setup lang="ts">
/** Composant "dumb" : toute la logique vit dans useCatalogueFilters. */
import { ref } from 'vue'
import { useCatalogueFilters } from '@/composables/useCatalogueFilters'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import type { RobotType, BaieType } from '@/types'
import { ChevronDown, ChevronUp, RotateCcw } from 'lucide-vue-next'

const { filters, rechercheLocale, updateFilter, resetAll, resultCount } = useCatalogueFilters()

const TYPES: RobotType[] = ['Articulé', 'Soudure arc', 'Palettisation', 'Peinture', 'Delta', 'Collaboratif']
const BAIES: BaieType[] = ['R-30iB', 'R-30iB Plus', 'R-30iA']
const AXES = [4, 5, 6, 7] as const

const showAdvanced = ref(false)

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
  <aside class="space-y-6">
    <div>
      <label class="block font-mono text-[11px] uppercase tracking-widest text-ran-graphite-400 mb-1.5">
        Recherche modèle
      </label>
      <BaseInput v-model="rechercheLocale" placeholder="Ex : ARC Mate, M-710iC…" />
    </div>

    <div>
      <span class="block font-mono text-[11px] uppercase tracking-widest text-ran-graphite-400 mb-1.5">Type de robot</span>
      <div class="flex flex-wrap gap-1.5">
        <button
          v-for="t in TYPES" :key="t" @click="toggleType(t)"
          class="px-2.5 py-1 text-xs border transition-colors"
          :class="filters.types.includes(t) ? 'border-ran-yellow-500 text-ran-yellow-500 bg-ran-yellow-500/10' : 'border-ran-graphite-600 text-ran-graphite-300 hover:border-ran-steel-500'"
        >{{ t }}</button>
      </div>
    </div>

    <button class="flex items-center gap-1.5 font-mono text-[11px] uppercase tracking-widest text-ran-steel-300 hover:text-ran-yellow-500" @click="showAdvanced = !showAdvanced">
      <component :is="showAdvanced ? ChevronUp : ChevronDown" class="size-3.5" />
      Afficher plus de filtres
    </button>

    <div v-if="showAdvanced" class="space-y-5 border-t border-ran-graphite-700 pt-5">
      <div>
        <span class="block font-mono text-[11px] uppercase tracking-widest text-ran-graphite-400 mb-1.5">Payload (kg)</span>
        <div class="grid grid-cols-2 gap-2">
          <BaseInput type="number" :model-value="String(filters.payloadKg?.min ?? '')" placeholder="min" @update:modelValue="v => updateFilter('payloadKg', { ...filters.payloadKg, min: v ? Number(v) : undefined })" />
          <BaseInput type="number" :model-value="String(filters.payloadKg?.max ?? '')" placeholder="max" @update:modelValue="v => updateFilter('payloadKg', { ...filters.payloadKg, max: v ? Number(v) : undefined })" />
        </div>
      </div>

      <div>
        <span class="block font-mono text-[11px] uppercase tracking-widest text-ran-graphite-400 mb-1.5">Rayon d'action (m)</span>
        <div class="grid grid-cols-2 gap-2">
          <BaseInput type="number" :model-value="String(filters.rayonActionM?.min ?? '')" placeholder="min" @update:modelValue="v => updateFilter('rayonActionM', { ...filters.rayonActionM, min: v ? Number(v) : undefined })" />
          <BaseInput type="number" :model-value="String(filters.rayonActionM?.max ?? '')" placeholder="max" @update:modelValue="v => updateFilter('rayonActionM', { ...filters.rayonActionM, max: v ? Number(v) : undefined })" />
        </div>
      </div>

      <div>
        <span class="block font-mono text-[11px] uppercase tracking-widest text-ran-graphite-400 mb-1.5">Nombre d'axes</span>
        <div class="flex gap-1.5">
          <button v-for="a in AXES" :key="a" @click="toggleAxe(a)" class="size-8 text-xs border transition-colors" :class="filters.axes.includes(a) ? 'border-ran-yellow-500 text-ran-yellow-500 bg-ran-yellow-500/10' : 'border-ran-graphite-600 text-ran-graphite-300 hover:border-ran-steel-500'">{{ a }}</button>
        </div>
      </div>

      <div>
        <span class="block font-mono text-[11px] uppercase tracking-widest text-ran-graphite-400 mb-1.5">Type de baie</span>
        <BaseSelect :model-value="filters.typeBaie ?? ''" :options="BAIES.map(b => ({ value: b, label: b }))" placeholder="Toutes" @update:modelValue="v => updateFilter('typeBaie', (v || undefined) as any)" />
      </div>
    </div>

    <div class="flex items-center justify-between border-t border-ran-graphite-700 pt-4">
      <span class="font-mono text-xs text-ran-graphite-400">{{ resultCount }} résultat(s)</span>
      <BaseButton variant="ghost" size="sm" @click="resetAll">
        <RotateCcw class="size-3.5" /> Réinitialiser
      </BaseButton>
    </div>
  </aside>
</template>
