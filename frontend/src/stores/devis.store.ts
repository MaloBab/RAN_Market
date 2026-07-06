import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { DevisRequest, DevisSubmissionResult } from '@/types'
import { devisService } from '@/services'

export const useDevisStore = defineStore('devis', () => {
  const isSubmitting = ref(false)
  const lastResult = ref<DevisSubmissionResult | null>(null)
  const error = ref<string | null>(null)

  async function submit(payload: DevisRequest) {
    isSubmitting.value = true
    error.value = null
    try {
      lastResult.value = await devisService.submit(payload)
      return lastResult.value
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Échec de l’envoi de la demande.'
      throw e
    } finally {
      isSubmitting.value = false
    }
  }

  function reset() {
    lastResult.value = null
    error.value = null
  }

  return { isSubmitting, lastResult, error, submit, reset }
})


