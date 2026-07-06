<script setup lang="ts">
import { RouterLink } from 'vue-router'
import ExcelImportPanel from '@/components/backoffice/ExcelImportPanel.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { PlusCircle } from 'lucide-vue-next'
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
    <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 mb-2">
      <div>
        <p class="text-sm font-semibold text-brand-red-600 mb-1">Back-office RAN</p>
        <h1 class="font-heading font-extrabold text-3xl sm:text-4xl tracking-tight text-ink-900">Import Excel — Fiches robots</h1>
      </div>
      <RouterLink to="/back-office/nouveau" class="shrink-0">
        <BaseButton variant="secondary" size="sm" class="w-full sm:w-auto">
          <PlusCircle class="size-4" aria-hidden="true" /> Créer une fiche manuellement
        </BaseButton>
      </RouterLink>
    </div>
    <p class="text-sm text-ink-500 mb-8">
      1 ligne = 1 robot. Les fiches créées sont en statut « Brouillon » jusqu'à validation manuelle.
    </p>
    <ExcelImportPanel />
  </div>
</template>
