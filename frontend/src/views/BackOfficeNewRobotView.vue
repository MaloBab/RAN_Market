<script setup lang="ts">
import { RouterLink } from 'vue-router'
import RobotForm from '@/components/backoffice/RobotForm.vue'
import { ArrowLeft } from 'lucide-vue-next'
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
    <RouterLink
      to="/back-office"
      class="inline-flex items-center gap-1.5 min-h-9 text-sm font-medium text-ink-500 hover:text-ink-900 mb-6 transition-colors"
    >
      <ArrowLeft class="size-3.5" aria-hidden="true" /> Retour au back-office
    </RouterLink>
    <p class="text-sm font-semibold text-brand-red-600 mb-1">Back-office RAN</p>
    <h1 class="font-heading font-extrabold text-3xl sm:text-4xl tracking-tight text-ink-900 mb-2">Nouvelle fiche robot</h1>
    <p class="text-sm text-ink-500 mb-8">
      Création manuelle — la fiche est enregistrée en statut « Brouillon » jusqu'à validation.
    </p>
    <RobotForm />
  </div>
</template>
