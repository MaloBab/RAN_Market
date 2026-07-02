<script setup lang="ts">
import { cn } from '@/utils/cn'

withDefaults(defineProps<{ bracket?: boolean; class?: string }>(), { bracket: false })
</script>

<template>
  <div :class="cn('bg-ran-graphite-900 border border-ran-graphite-700', bracket && 'ran-bracket', $props.class)">
    <slot />
  </div>
</template>
