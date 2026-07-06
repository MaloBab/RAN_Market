<script setup lang="ts">
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useBackofficeStore } from '@/stores/backoffice.store'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import { UploadCloud, FileSpreadsheet, CheckCircle2, XCircle, Copy } from 'lucide-vue-next'

const store = useBackofficeStore()
const { phase, progress, report, error } = storeToRefs(store)

const fileInput = ref<HTMLInputElement | null>(null)
const dragOver = ref(false)
const fileName = ref<string | null>(null)

const isBusy = computed(() => phase.value === 'uploading' || phase.value === 'parsing')

function pickFile() {
  fileInput.value?.click()
}

function handleFile(file: File | undefined) {
  if (!file) return
  fileName.value = file.name
  store.importFile(file)
}

function onDrop(e: DragEvent) {
  dragOver.value = false
  handleFile(e.dataTransfer?.files?.[0])
}
</script>

<template>
  <div class="space-y-5">
    <BaseCard
      class="border-2 border-dashed p-8 flex flex-col items-center justify-center gap-3 text-center transition-colors duration-150"
      :class="dragOver ? 'border-brand-red-600 bg-brand-red-100/40' : 'border-ink-200'"
      @dragover.prevent="dragOver = true"
      @dragleave.prevent="dragOver = false"
      @drop.prevent="onDrop"
    >
      <UploadCloud class="size-8 text-ink-400" aria-hidden="true" />
      <div>
        <p class="text-sm text-ink-700">Glissez-déposez le fichier Excel préformaté</p>
        <p class="text-xs text-ink-400">ou</p>
      </div>
      <BaseButton variant="secondary" size="sm" @click="pickFile" :disabled="isBusy">
        Choisir un fichier .xlsx
      </BaseButton>
      <a href="#" class="text-xs text-ink-500 hover:text-brand-red-600 underline underline-offset-2 min-h-9 flex items-center">
        Télécharger le modèle Excel
      </a>
      <input
        ref="fileInput"
        type="file"
        accept=".xlsx,.xls"
        class="hidden"
        aria-label="Fichier Excel de fiches robots"
        @change="handleFile(($event.target as HTMLInputElement).files?.[0])"
      />
    </BaseCard>

    <div v-if="fileName" class="flex items-center gap-2 text-sm text-ink-700">
      <FileSpreadsheet class="size-4 text-ink-500" aria-hidden="true" /> {{ fileName }}
    </div>

    <div v-if="isBusy" class="space-y-2">
      <div class="flex items-center justify-between text-xs font-medium text-ink-500">
        <span>{{ phase === 'uploading' ? 'Envoi du fichier…' : 'Analyse des lignes…' }}</span>
        <span>{{ progress }}%</span>
      </div>
      <div class="h-1.5 w-full rounded-full bg-ink-100 overflow-hidden" role="progressbar" :aria-valuenow="progress" aria-valuemin="0" aria-valuemax="100">
        <div class="h-full rounded-full bg-brand-red-600 transition-all duration-150" :style="{ width: `${progress}%` }" />
      </div>
    </div>

    <div v-if="error" class="flex items-center gap-2 text-sm text-danger-600 rounded-lg border border-danger-100 bg-danger-100/60 px-3.5 py-2.5" role="alert">
      <XCircle class="size-4 shrink-0" aria-hidden="true" /> {{ error }}
    </div>

    <div v-if="report" class="space-y-4">
      <div class="grid grid-cols-3 gap-2 sm:gap-3">
        <BaseCard class="p-3 text-center">
          <p class="font-heading font-bold text-xl sm:text-2xl text-ink-900">{{ report.totalLignes }}</p>
          <p class="text-[10px] font-medium uppercase tracking-wide text-ink-500">Lignes lues</p>
        </BaseCard>
        <BaseCard class="p-3 text-center border-ok-100">
          <p class="font-heading font-bold text-xl sm:text-2xl text-ok-600">{{ report.accepte }}</p>
          <p class="text-[10px] font-medium uppercase tracking-wide text-ink-500">Acceptées</p>
        </BaseCard>
        <BaseCard class="p-3 text-center border-danger-100">
          <p class="font-heading font-bold text-xl sm:text-2xl text-danger-600">{{ report.erreurs + report.doublons }}</p>
          <p class="text-[10px] font-medium uppercase tracking-wide text-ink-500">Erreurs / doublons</p>
        </BaseCard>
      </div>

      <BaseCard class="max-h-72 overflow-y-auto divide-y divide-ink-100">
        <div v-for="row in report.details.filter(d => d.statut !== 'accepte')" :key="row.ligne" class="flex items-start gap-3 px-3.5 py-2.5 text-xs">
          <component :is="row.statut === 'erreur' ? XCircle : Copy" class="size-4 mt-0.5 shrink-0" :class="row.statut === 'erreur' ? 'text-danger-600' : 'text-ink-400'" aria-hidden="true" />
          <div class="flex-1">
            <span class="font-mono text-ink-700">Ligne {{ row.ligne }} · {{ row.idRobot }}</span>
            <p class="text-ink-500">{{ row.message }}</p>
          </div>
          <BaseBadge :tone="row.statut === 'erreur' ? 'alert' : 'neutral'">{{ row.statut }}</BaseBadge>
        </div>
        <div v-if="report.accepte > 0" class="flex items-center gap-2 px-3.5 py-2.5 text-xs text-ok-600">
          <CheckCircle2 class="size-4" aria-hidden="true" /> {{ report.accepte }} fiche(s) créée(s) en statut « Brouillon »
        </div>
      </BaseCard>

      <BaseButton variant="ghost" size="sm" @click="store.reset(); fileName = null">Nouvel import</BaseButton>
    </div>
  </div>
</template>
