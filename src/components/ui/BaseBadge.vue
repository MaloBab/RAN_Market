<script setup lang="ts">
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/utils/cn'

const badge = cva('inline-flex items-center gap-1 px-2 py-0.5 text-[11px] font-mono uppercase tracking-wide border', {
  variants: {
    tone: {
      neutral: 'border-ran-graphite-600 text-ran-graphite-200',
      yellow: 'border-ran-yellow-500 text-ran-yellow-500',
      ok: 'border-ran-ok-500 text-ran-ok-500',
      alert: 'border-ran-alert-500 text-ran-alert-500',
      steel: 'border-ran-steel-500 text-ran-steel-300'
    }
  },
  defaultVariants: { tone: 'neutral' }
})

defineProps<{ tone?: VariantProps<typeof badge>['tone'] }>()
</script>

<template>
  <span :class="cn(badge({ tone }))"><slot /></span>
</template>
