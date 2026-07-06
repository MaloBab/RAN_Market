<script setup lang="ts">
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/utils/cn'
import { Loader2 } from 'lucide-vue-next'

const button = cva(
  'inline-flex items-center justify-center gap-2 rounded-lg font-semibold cursor-pointer select-none transition-all duration-150 ease-[var(--ease-ran)] active:scale-[0.98] disabled:opacity-40 disabled:pointer-events-none disabled:cursor-not-allowed focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-red-600 focus-visible:ring-offset-2',
  {
    variants: {
      variant: {
        primary: 'bg-brand-red-600 text-white shadow-sm hover:bg-brand-red-700',
        secondary: 'bg-white text-ink-900 border border-ink-200 shadow-sm hover:border-ink-300 hover:bg-ink-50',
        ghost: 'text-ink-700 hover:text-ink-900 hover:bg-ink-100',
        outline: 'border border-brand-red-600 text-brand-red-600 hover:bg-brand-red-100/60',
        danger: 'border border-danger-600 text-danger-600 hover:bg-danger-100'
      },
      size: {
        sm: 'text-sm px-3 min-h-9',
        md: 'text-sm px-4 min-h-11',
        lg: 'text-[15px] px-6 min-h-12'
      }
    },
    defaultVariants: { variant: 'primary', size: 'md' }
  }
)

type ButtonVariants = VariantProps<typeof button>

withDefaults(
  defineProps<{
    variant?: ButtonVariants['variant']
    size?: ButtonVariants['size']
    type?: 'button' | 'submit'
    loading?: boolean
    disabled?: boolean
  }>(),
  { variant: 'primary', size: 'md', type: 'button', loading: false, disabled: false }
)
</script>

<template>
  <button :type="type" :disabled="loading || disabled" :class="cn(button({ variant, size }))">
    <Loader2 v-if="loading" class="size-4 animate-spin" aria-hidden="true" />
    <slot />
  </button>
</template>
