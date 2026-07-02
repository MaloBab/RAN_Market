<script setup lang="ts">
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/utils/cn'

/**
 * Bouton mutualisé (DRY) — toute l'app passe par ce composant pour
 * garantir une cohérence visuelle et un focus clavier accessible.
 */
const button = cva(
  'inline-flex items-center justify-center gap-2 font-medium transition-colors duration-150 disabled:opacity-40 disabled:pointer-events-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ran-yellow-500 focus-visible:ring-offset-2 focus-visible:ring-offset-ran-graphite-950',
  {
    variants: {
      variant: {
        primary: 'bg-ran-yellow-500 text-ran-graphite-950 hover:bg-ran-yellow-400',
        secondary: 'bg-ran-graphite-800 text-ran-graphite-100 border border-ran-graphite-600 hover:border-ran-steel-500',
        ghost: 'text-ran-graphite-200 hover:text-ran-yellow-500',
        outline: 'border border-ran-yellow-500 text-ran-yellow-500 hover:bg-ran-yellow-500/10'
      },
      size: {
        sm: 'text-xs px-3 py-1.5',
        md: 'text-sm px-4 py-2.5',
        lg: 'text-sm px-6 py-3'
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
  }>(),
  { variant: 'primary', size: 'md', type: 'button' }
)
</script>

<template>
  <button :type="type" :class="cn(button({ variant, size }))">
    <slot />
  </button>
</template>
