<script setup lang="ts">
/** Barre flottante récapitulant la sélection pour le comparateur (§3.4). */
import { RouterLink } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useRobotsStore } from '@/stores/robots.store'
import BaseButton from '@/components/ui/BaseButton.vue'
import { X, GitCompareArrows } from 'lucide-vue-next'

const store = useRobotsStore()
const { compareRobots } = storeToRefs(store)
</script>

<template>
  <Transition enter-active-class="transition-all duration-200" enter-from-class="opacity-0 translate-y-4" leave-active-class="transition-all duration-150" leave-to-class="opacity-0 translate-y-4">
    <div
      v-if="compareRobots.length > 0"
      class="fixed bottom-5 left-1/2 -translate-x-1/2 z-30 flex flex-wrap items-center justify-center gap-3 sm:gap-4 max-w-[calc(100vw-2rem)] bg-white rounded-2xl border border-ink-200 px-4 sm:px-5 py-3 shadow-[var(--shadow-popover)]"
      role="status"
    >
      <GitCompareArrows class="size-4 text-brand-red-600 shrink-0" aria-hidden="true" />
      <div class="flex flex-wrap items-center gap-2">
        <div v-for="r in compareRobots" :key="r.id" class="flex items-center gap-1.5 rounded-full bg-ink-100 pl-3 pr-1 min-h-9 text-xs font-medium text-ink-700">
          {{ r.modele }}
          <button
            @click="store.toggleCompare(r.id)"
            class="p-1.5 rounded-full text-ink-400 hover:text-brand-red-600 hover:bg-white transition-colors cursor-pointer"
            :aria-label="`Retirer ${r.modele} de la comparaison`"
          >
            <X class="size-3" aria-hidden="true" />
          </button>
        </div>
      </div>
      <RouterLink to="/comparateur">
        <BaseButton size="sm" :disabled="compareRobots.length < 2">Comparer</BaseButton>
      </RouterLink>
    </div>
  </Transition>
</template>
