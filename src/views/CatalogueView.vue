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
  <div class="max-w-7xl mx-auto px-6 py-8">
    <div class="mb-8">
      <p class="font-mono text-xs uppercase tracking-widest text-ran-yellow-500 mb-1">Robots reconditionnés — FANUC RAN</p>
      <h1 class="font-display text-4xl tracking-wide text-ran-graphite-100">Catalogue robots</h1>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-[260px_1fr] gap-8">
      <FiltersPanel />
      <RobotGrid :robots="robots" :is-loading="isLoading" />
    </div>

    <CompareBar />
  </div>
</template>
