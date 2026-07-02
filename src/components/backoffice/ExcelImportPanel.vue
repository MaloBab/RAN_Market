<script setup lang="ts">
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useBackofficeStore } from '@/stores/backoffice.store'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
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
    <div
      class="border-2 border-dashed p-8 flex flex-col items-center justify-center gap-3 text-center transition-colors"
      :class="dragOver ? 'border-ran-yellow-500 bg-ran-yellow-500/5' : 'border-ran-graphite-600'"
      @dragover.prevent="dragOver = true"
      @dragleave.prevent="dragOver = false"
      @drop.prevent="onDrop"
    >
      <UploadCloud class="size-8 text-ran-graphite-400" />
      <div>
        <p class="text-sm text-ran-graphite-200">Glissez-déposez le fichier Excel préformaté</p>
        <p class="text-xs text-ran-graphite-500">ou</p>
      </div>
      <BaseButton variant="secondary" size="sm" @click="pickFile" :disabled="isBusy">
        Choisir un fichier .xlsx
      </BaseButton>
      <a href="#" class="text-xs text-ran-steel-300 hover:text-ran-yellow-500 underline underline-offset-2">
        Télécharger le modèle Excel
      </a>
      <input ref="fileInput" type="file" accept=".xlsx,.xls" class="hidden" @change="handleFile(($event.target as HTMLInputElement).files?.[0])" />
    </div>

    <div v-if="fileName" class="flex items-center gap-2 text-sm text-ran-graphite-300">
      <FileSpreadsheet class="size-4 text-ran-steel-300" /> {{ fileName }}
    </div>

    <div v-if="isBusy" class="space-y-2">
      <div class="flex items-center justify-between text-xs font-mono text-ran-graphite-400">
        <span>{{ phase === 'uploading' ? 'Envoi du fichier…' : 'Analyse des lignes…' }}</span>
        <span>{{ progress }}%</span>
      </div>
      <div class="h-1.5 w-full bg-ran-graphite-800 overflow-hidden">
        <div class="h-full bg-ran-yellow-500 transition-all duration-150" :style="{ width: `${progress}%` }" />
      </div>
    </div>

    <div v-if="error" class="flex items-center gap-2 text-sm text-ran-alert-500 border border-ran-alert-500/40 bg-ran-alert-500/5 px-3 py-2">
      <XCircle class="size-4" /> {{ error }}
    </div>

    <div v-if="report" class="space-y-4">
      <div class="grid grid-cols-3 gap-3">
        <div class="bg-ran-graphite-900 border border-ran-graphite-700 p-3 text-center">
          <p class="font-display text-2xl text-ran-graphite-100">{{ report.totalLignes }}</p>
          <p class="text-[10px] font-mono uppercase tracking-wider text-ran-graphite-500">Lignes lues</p>
        </div>
        <div class="bg-ran-graphite-900 border border-ran-ok-500/40 p-3 text-center">
          <p class="font-display text-2xl text-ran-ok-500">{{ report.accepte }}</p>
          <p class="text-[10px] font-mono uppercase tracking-wider text-ran-graphite-500">Acceptées</p>
        </div>
        <div class="bg-ran-graphite-900 border border-ran-alert-500/40 p-3 text-center">
          <p class="font-display text-2xl text-ran-alert-500">{{ report.erreurs + report.doublons }}</p>
          <p class="text-[10px] font-mono uppercase tracking-wider text-ran-graphite-500">Erreurs / doublons</p>
        </div>
      </div>

      <div class="max-h-72 overflow-y-auto border border-ran-graphite-700 divide-y divide-ran-graphite-800">
        <div v-for="row in report.details.filter(d => d.statut !== 'accepte')" :key="row.ligne" class="flex items-start gap-3 px-3 py-2 text-xs">
          <component :is="row.statut === 'erreur' ? XCircle : Copy" class="size-4 mt-0.5 shrink-0" :class="row.statut === 'erreur' ? 'text-ran-alert-500' : 'text-ran-steel-300'" />
          <div class="flex-1">
            <span class="font-mono text-ran-graphite-300">Ligne {{ row.ligne }} · {{ row.idRobot }}</span>
            <p class="text-ran-graphite-500">{{ row.message }}</p>
          </div>
          <BaseBadge :tone="row.statut === 'erreur' ? 'alert' : 'steel'">{{ row.statut }}</BaseBadge>
        </div>
        <div v-if="report.accepte > 0" class="flex items-center gap-2 px-3 py-2 text-xs text-ran-ok-500">
          <CheckCircle2 class="size-4" /> {{ report.accepte }} fiche(s) créée(s) en statut « Brouillon »
        </div>
      </div>

      <BaseButton variant="ghost" size="sm" @click="store.reset(); fileName = null">Nouvel import</BaseButton>
    </div>
  </div>
</template>
