<script setup lang="ts">
import { RouterLink } from 'vue-router'
import ExcelImportPanel from '@/components/backoffice/ExcelImportPanel.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { PlusCircle } from 'lucide-vue-next'
</script>

<template>
  <div class="max-w-3xl mx-auto px-6 py-8">
    <div class="flex items-start justify-between gap-4 mb-2">
      <div>
        <p class="font-mono text-xs uppercase tracking-widest text-ran-yellow-500 mb-1">Back-office RAN</p>
        <h1 class="font-display text-4xl tracking-wide text-ran-graphite-100">Import Excel — Fiches robots</h1>
      </div>
      <RouterLink to="/back-office/nouveau">
        <BaseButton variant="secondary" size="sm">
          <PlusCircle class="size-4" /> Créer une fiche manuellement
        </BaseButton>
      </RouterLink>
    </div>
    <p class="text-sm text-ran-graphite-400 mb-8">
      1 ligne = 1 robot. Les fiches créées sont en statut « Brouillon » jusqu'à validation manuelle.
    </p>
    <ExcelImportPanel />
  </div>
</template>
