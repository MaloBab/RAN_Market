<script setup lang="ts">
import type { Robot } from '@/types'
import RobotCard from './RobotCard.vue'
import { PackageSearch } from 'lucide-vue-next'

defineProps<{ robots: Robot[]; isLoading: boolean }>()
</script>

<template>
  <div v-if="isLoading" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5" aria-hidden="true">
    <div v-for="i in 6" :key="i" class="aspect-[4/3] rounded-xl bg-white border border-ink-200 animate-pulse" />
  </div>

  <div v-else-if="robots.length === 0" class="flex flex-col items-center justify-center py-24 text-center gap-3 rounded-xl border border-dashed border-ink-200 bg-white">
    <PackageSearch class="size-10 text-ink-300" aria-hidden="true" />
    <p class="font-heading font-semibold text-xl text-ink-700">Aucun robot ne correspond à ces critères</p>
    <p class="text-sm text-ink-500">Essayez d'élargir vos filtres ou de réinitialiser la recherche.</p>
  </div>

  <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
    <RobotCard v-for="robot in robots" :key="robot.id" :robot="robot" />
  </div>
</template>
