<script setup lang="ts">
import { cn } from '@/utils/cn'

withDefaults(
  defineProps<{ interactive?: boolean; class?: string; as?: string }>(),
  { interactive: false, as: 'div' }
)
</script>

<template>
  <component
    :is="as"
    :class="cn(
      'bg-surface border border-ink-200 rounded-xl shadow-[var(--shadow-card)] transition-[box-shadow,border-color,transform] duration-200 ease-[var(--ease-ran)]',
      interactive && 'hover:shadow-[var(--shadow-card-hover)] hover:border-ink-300 hover:-translate-y-0.5 focus-within:shadow-[var(--shadow-card-hover)]',
      $props.class
    )"
  >
    <slot />
  </component>
</template>
