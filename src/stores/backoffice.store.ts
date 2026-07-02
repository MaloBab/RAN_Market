import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ImportPhase, ImportReport } from '@/types'
import { importService } from '@/services'

export const useBackofficeStore = defineStore('backoffice', () => {
  const phase = ref<ImportPhase>('idle')
  const progress = ref(0)
  const report = ref<ImportReport | null>(null)
  const error = ref<string | null>(null)

  async function importFile(file: File) {
    phase.value = 'uploading'
    progress.value = 0
    error.value = null
    report.value = null
    try {
      phase.value = 'parsing'
      report.value = await importService.importExcel(file, (pct) => {
        progress.value = pct
      })
      phase.value = 'done'
    } catch (e) {
      phase.value = 'failed'
      error.value = e instanceof Error ? e.message : 'Échec de l’import.'
    }
  }

  function reset() {
    phase.value = 'idle'
    progress.value = 0
    report.value = null
    error.value = null
  }

  return { phase, progress, report, error, importFile, reset }
})
