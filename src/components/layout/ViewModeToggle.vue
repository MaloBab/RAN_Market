<script setup lang="ts">
/**
 * Toggle Commerciale ↔ Client (CDC §5.2). Visible uniquement si
 * `canToggleView` (= utilisateur Commercial authentifié).
 */
import { useViewStrategy } from '@/composables/useViewStrategy'
import BaseBadge from '@/components/ui/BaseBadge.vue'

const { effectiveDisplayMode, canToggleView, toggle } = useViewStrategy()
</script>

<template>
  <button
    v-if="canToggleView"
    @click="toggle"
    class="group flex items-center gap-3 border border-ran-graphite-600 px-3 py-1.5 hover:border-ran-yellow-500 transition-colors"
    :aria-pressed="effectiveDisplayMode === 'client'"
  >
    <span class="font-mono text-[11px] uppercase tracking-widest text-ran-graphite-400">Vue</span>
    <span class="relative flex items-center w-27 h-7 bg-ran-graphite-800 border border-ran-graphite-600">
      <span
        class="absolute top-0 bottom-0 w-1/2 bg-ran-yellow-500 transition-transform duration-200"
        :class="effectiveDisplayMode === 'client' ? 'translate-x-full' : 'translate-x-0'"
      />
      <span class="relative z-10 w-1/2 text-center text-[11px] font-mono" :class="effectiveDisplayMode === 'commerciale' ? 'text-ran-graphite-950 font-semibold' : 'text-ran-graphite-300'">COM</span>
      <span class="relative z-10 w-1/2 text-center text-[11px] font-mono" :class="effectiveDisplayMode === 'client' ? 'text-ran-graphite-950 font-semibold' : 'text-ran-graphite-300'">CLI</span>
    </span>
    <BaseBadge v-if="effectiveDisplayMode === 'client'" tone="steel">démo</BaseBadge>
  </button>
</template>
