<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useRobotsStore } from '@/stores/robots.store'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import { Clock, BellRing } from 'lucide-vue-next'

const store = useRobotsStore()
const { comingSoon } = storeToRefs(store)
onMounted(() => store.fetchComingSoon())
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
    <p class="text-sm font-semibold text-brand-red-600 mb-1">Réservé à la vue commerciale</p>
    <h1 class="font-heading font-extrabold text-3xl sm:text-4xl tracking-tight text-ink-900 mb-8">Coming Soon</h1>

    <div v-if="!comingSoon?.length" class="text-ink-500 py-16 text-center">Aucune entrée à venir pour le moment.</div>

    <div v-else class="grid sm:grid-cols-2 gap-4">
      <BaseCard v-for="entry in comingSoon" :key="entry.id" interactive class="p-4 space-y-3">
        <div class="flex items-center justify-between">
          <BaseBadge tone="yellow">{{ entry.type }}</BaseBadge>
          <span class="flex items-center gap-1 text-xs font-medium text-ink-500">
            <Clock class="size-3.5" aria-hidden="true" />{{ entry.disponibiliteEstimee }}
          </span>
        </div>
        <h3 class="font-heading font-semibold text-xl text-ink-900">{{ entry.modele }}</h3>
        <p class="text-xs text-ink-500">Rénovation prévue : {{ entry.niveauRenovationPrevu }}</p>
        <button class="flex items-center gap-1.5 min-h-9 text-xs font-semibold text-ink-600 hover:text-brand-red-600 transition-colors cursor-pointer pt-2 border-t border-ink-100 w-full">
          <BellRing class="size-3.5" aria-hidden="true" /> Alerter un client
        </button>
      </BaseCard>
    </div>
  </div>
</template>
