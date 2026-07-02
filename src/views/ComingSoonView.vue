<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useRobotsStore } from '@/stores/robots.store'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import { Clock } from 'lucide-vue-next'

const store = useRobotsStore()
const { comingSoon } = storeToRefs(store)
onMounted(() => store.fetchComingSoon())
</script>

<template>
  <div class="max-w-5xl mx-auto px-6 py-8">
    <p class="font-mono text-xs uppercase tracking-widest text-ran-yellow-500 mb-1">Réservé à la vue commerciale</p>
    <h1 class="font-display text-4xl tracking-wide text-ran-graphite-100 mb-8">Coming Soon</h1>

    <div class="grid sm:grid-cols-2 gap-4">
      <BaseCard v-for="entry in comingSoon" :key="entry.id" class="p-4 space-y-2">
        <div class="flex items-center justify-between">
          <BaseBadge tone="yellow">{{ entry.type }}</BaseBadge>
          <span class="flex items-center gap-1 text-xs font-mono text-ran-steel-300"><Clock class="size-3.5" />{{ entry.disponibiliteEstimee }}</span>
        </div>
        <h3 class="font-display text-xl text-ran-graphite-100">{{ entry.modele }}</h3>
        <p class="text-xs text-ran-graphite-400">Rénovation prévue : {{ entry.niveauRenovationPrevu }}</p>
      </BaseCard>
    </div>
  </div>
</template>
