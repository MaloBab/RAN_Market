<script setup lang="ts">
import { useRoute } from 'vue-router'
import DevisForm from '@/components/devis/DevisForm.vue'
import type { NiveauRenovation } from '@/types'

const route = useRoute()
const robotId = route.query.robotId as string | undefined
const prestationsDisponibles: NiveauRenovation[] = ['Standard', 'Premium', 'Quasi Neuve', 'Peinture', 'Extension de garantie', 'Échange standard']
</script>

<template>
  <div class="max-w-2xl mx-auto px-6 py-8">
    <h1 class="font-display text-4xl tracking-wide text-ran-graphite-100 mb-2">Demande de devis</h1>
    <p class="text-sm text-ran-graphite-400 mb-8">Un commercial FANUC vous recontacte sous 48h ouvrées.</p>
    <DevisForm :robot-id="robotId" :prestations-disponibles="prestationsDisponibles" />
  </div>
</template>
