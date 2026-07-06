import { reactive } from 'vue'
import type { DevisRequest, NiveauRenovation } from '@/types'
import { useDevisStore } from '@/stores/devis.store'

/**
 * Pré-remplissage conditionnel (CDC §3.8) : si `robotId` est fourni
 * (accès depuis une fiche robot), le formulaire l'embarque directement.
 */
export function useDevisForm(robotId?: string) {
  const store = useDevisStore()

  const form = reactive<DevisRequest>({
    prenom: '',
    nom: '',
    email: '',
    telephone: '',
    pays: '',
    societe: '',
    fonction: '',
    robotId,
    prestationsSouhaitees: [] as NiveauRenovation[],
    demandeSpeciale: ''
  })

  function togglePrestation(p: NiveauRenovation) {
    const i = form.prestationsSouhaitees.indexOf(p)
    if (i >= 0) form.prestationsSouhaitees.splice(i, 1)
    else form.prestationsSouhaitees.push(p)
  }

  async function submit() {
    return store.submit({ ...form })
  }

  return { form, togglePrestation, submit, isSubmitting: store.isSubmitting, lastResult: store.lastResult, error: store.error }
}


