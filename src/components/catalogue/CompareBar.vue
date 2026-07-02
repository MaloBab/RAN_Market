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
    <div v-if="compareRobots.length > 0" class="fixed bottom-5 left-1/2 -translate-x-1/2 z-30 flex items-center gap-4 bg-ran-graphite-900 border border-ran-yellow-500 px-5 py-3 shadow-xl shadow-black/40">
      <GitCompareArrows class="size-4 text-ran-yellow-500" />
      <div class="flex items-center gap-2">
        <div v-for="r in compareRobots" :key="r.id" class="flex items-center gap-1.5 bg-ran-graphite-800 pl-2 pr-1 py-1 text-xs">
          {{ r.modele }}
          <button @click="store.toggleCompare(r.id)" class="text-ran-graphite-400 hover:text-ran-alert-500"><X class="size-3" /></button>
        </div>
      </div>
      <RouterLink to="/comparateur">
        <BaseButton size="sm" :disabled="compareRobots.length < 2">Comparer</BaseButton>
      </RouterLink>
    </div>
  </Transition>
</template>
