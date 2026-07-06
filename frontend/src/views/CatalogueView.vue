<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useRobotsStore } from '@/stores/robots.store'
import FiltersPanel from '@/components/catalogue/FiltersPanel.vue'
import RobotGrid from '@/components/catalogue/RobotGrid.vue'
import CompareBar from '@/components/catalogue/CompareBar.vue'

const store = useRobotsStore()
const { robots, isLoading } = storeToRefs(store)

onMounted(() => store.fetchRobots())
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 py-6 sm:py-8 pb-24">
    <div class="mb-6 sm:mb-8">
      <p class="text-sm font-semibold text-brand-red-600 mb-1">Robots reconditionnés — FANUC RAN</p>
      <h1 class="font-heading font-extrabold text-3xl sm:text-4xl tracking-tight text-ink-900">Catalogue robots</h1>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-6 lg:gap-8">
      <FiltersPanel />
      <RobotGrid :robots="robots" :is-loading="isLoading" />
    </div>

    <CompareBar />
  </div>
</template>
