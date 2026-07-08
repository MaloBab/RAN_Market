<script setup lang="ts">
/**
 * Toggle Commerciale ↔ Client (CDC §5.2). Visible uniquement si
 * `canToggleView` (= utilisateur Commercial authentifié).
 */
import { useViewStrategy } from '@/composables/useViewStrategy'

const { effectiveDisplayMode, canToggleView, toggle } = useViewStrategy()
</script>

<template>
  <button
    v-if="canToggleView"
    @click="toggle"
    class="group flex items-center gap-2.5 rounded-lg border border-ink-200 pl-3 pr-2 min-h-11 hover:border-ink-300 hover:bg-ink-50 transition-colors cursor-pointer"
    :aria-pressed="effectiveDisplayMode === 'client'"
    :aria-label="`Basculer en vue ${effectiveDisplayMode === 'commerciale' ? 'client' : 'commerciale'}`"
  >
    <span class="text-xs font-medium text-ink-500">Vue</span>
    <span class="relative flex items-center w-24 h-7 rounded-full bg-ink-100 border border-ink-200">
      <span
        class="absolute top-0.5 bottom-0.5 w-1/2 rounded-full bg-white shadow-sm transition-transform duration-200"
        :class="effectiveDisplayMode === 'client' ? 'translate-x-full' : 'translate-x-0.5'"
        style="width: calc(50% - 4px)"
      />
      <span class="relative z-10 w-1/2 text-center text-[11px] font-semibold" :class="effectiveDisplayMode === 'commerciale' ? 'text-ink-900' : 'text-ink-400'">COM</span>
      <span class="relative z-10 w-1/2 text-center text-[11px] font-semibold" :class="effectiveDisplayMode === 'client' ? 'text-ink-900' : 'text-ink-400'">CLI</span>
    </span>
  </button>
</template>
