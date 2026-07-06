<script setup lang="ts">
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/utils/cn'

const badge = cva('inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold leading-none', {
  variants: {
    tone: {
      neutral: 'bg-ink-100 text-ink-700',
      yellow: 'bg-brand-yellow-100 text-warn-700',
      red: 'bg-brand-red-100 text-brand-red-700',
      ok: 'bg-ok-100 text-ok-600',
      alert: 'bg-danger-100 text-danger-600'
    }
  },
  defaultVariants: { tone: 'neutral' }
})

defineProps<{ tone?: VariantProps<typeof badge>['tone'] }>()
</script>

<template>
  <span :class="cn(badge({ tone }))"><slot /></span>
</template>
