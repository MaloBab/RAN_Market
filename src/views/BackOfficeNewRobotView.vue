<script setup lang="ts">
import { RouterLink } from 'vue-router'
import RobotForm from '@/components/backoffice/RobotForm.vue'
import { ArrowLeft } from 'lucide-vue-next'
</script>

<template>
  <div class="max-w-3xl mx-auto px-6 py-8">
    <RouterLink to="/back-office" class="inline-flex items-center gap-1.5 text-xs font-mono uppercase tracking-wider text-ran-graphite-400 hover:text-ran-yellow-500 mb-6">
      <ArrowLeft class="size-3.5" /> Retour au back-office
    </RouterLink>
    <p class="font-mono text-xs uppercase tracking-widest text-ran-yellow-500 mb-1">Back-office RAN</p>
    <h1 class="font-display text-4xl tracking-wide text-ran-graphite-100 mb-2">Nouvelle fiche robot</h1>
    <p class="text-sm text-ran-graphite-400 mb-8">
      Création manuelle — la fiche est enregistrée en statut « Brouillon » jusqu'à validation.
    </p>
    <RobotForm />
  </div>
</template>
