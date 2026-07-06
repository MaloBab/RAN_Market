<script setup lang="ts">
import { useRoute } from 'vue-router'
import DevisForm from '@/components/devis/DevisForm.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import type { NiveauRenovation } from '@/types'

const route = useRoute()
const robotId = route.query.robotId as string | undefined
const prestationsDisponibles: NiveauRenovation[] = ['Standard', 'Premium', 'Quasi Neuve', 'Peinture', 'Extension de garantie', 'Échange standard']
</script>

<template>
  <div class="max-w-2xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
    <h1 class="font-heading font-extrabold text-3xl sm:text-4xl tracking-tight text-ink-900 mb-2">Demande de devis</h1>
    <p class="text-sm text-ink-500 mb-8">Un commercial FANUC vous recontacte sous 48h ouvrées.</p>
    <BaseCard class="p-5 sm:p-6">
      <DevisForm :robot-id="robotId" :prestations-disponibles="prestationsDisponibles" />
    </BaseCard>
  </div>
</template>
