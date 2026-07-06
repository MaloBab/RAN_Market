import { reactive, ref } from 'vue'
import type { BaieType, NiveauRenovation, Robot, RobotType } from '@/types'
import { robotService } from '@/services'

/**
 * Formulaire structuré de création manuelle de fiche robot (CDC §2.3).
 * Complémentaire à l'import Excel — même règle métier : la fiche créée
 * démarre en statut "Brouillon".
 */
export interface RobotFormState {
  id: string
  modele: string
  type: RobotType | ''
  categorie: string
  anneeMiseEnService: number | null
  heuresUtilisation: number | null
  descriptionCourte: string
  payloadKg: number | null
  rayonActionMm: number | null
  axes: 4 | 5 | 6 | 7 | null
  typeBaie: BaieType | ''
  protectionIp: string
  montage: string
  prixCatalogueEUR: number | null
  remisePct: number | null
  quantiteStock: number | null
  prestations: NiveauRenovation[]
}

const EMPTY: RobotFormState = {
  id: '', modele: '', type: '', categorie: '',
  anneeMiseEnService: null, heuresUtilisation: null, descriptionCourte: '',
  payloadKg: null, rayonActionMm: null, axes: null, typeBaie: '',
  protectionIp: '', montage: '',
  prixCatalogueEUR: null, remisePct: null, quantiteStock: null,
  prestations: []
}

export function useRobotForm() {
  const form = reactive<RobotFormState>({ ...EMPTY })
  const isSubmitting = ref(false)
  const error = ref<string | null>(null)
  const created = ref<Robot | null>(null)

  function togglePrestation(p: NiveauRenovation) {
    const i = form.prestations.indexOf(p)
    if (i >= 0) form.prestations.splice(i, 1)
    else form.prestations.push(p)
  }

  function validate(): string | null {
    if (!form.id.trim()) return 'ID robot obligatoire.'
    if (!form.modele.trim()) return 'Modèle obligatoire.'
    if (!form.type) return 'Type de robot obligatoire.'
    if (!form.axes) return "Nombre d'axes obligatoire."
    if (!form.typeBaie) return 'Type de baie obligatoire.'
    if (form.payloadKg === null || form.payloadKg <= 0) return 'Payload invalide.'
    if (form.rayonActionMm === null || form.rayonActionMm <= 0) return "Rayon d'action invalide."
    if (form.prixCatalogueEUR === null || form.prixCatalogueEUR <= 0) return 'Prix catalogue invalide.'
    if (form.descriptionCourte.length > 300) return 'Description trop longue (300 caractères max).'
    return null
  }

  async function submit() {
    const validationError = validate()
    if (validationError) {
      error.value = validationError
      return
    }
    isSubmitting.value = true
    error.value = null
    try {
      created.value = await robotService.create({
        id: form.id.trim(),
        modele: form.modele.trim(),
        type: form.type as RobotType,
        categorie: form.categorie.trim() || (form.type as string),
        anneeMiseEnService: form.anneeMiseEnService ?? new Date().getFullYear(),
        heuresUtilisation: form.heuresUtilisation ?? 0,
        descriptionCourte: form.descriptionCourte,
        caracteristiques: {
          payloadKg: form.payloadKg!,
          rayonActionMm: form.rayonActionMm!,
          axes: form.axes!,
          typeBaie: form.typeBaie as BaieType,
          protectionIp: form.protectionIp || 'Non renseigné',
          montage: form.montage || 'Non renseigné'
        },
        prestationsDisponibles: form.prestations.map((niveau) => ({ niveau, garantieMois: null })),
        media: { photosAvant: [], galerieAvantApres: [] },
        documentation: {},
        commercial: {
          prixCatalogueEUR: form.prixCatalogueEUR!,
          remisePct: form.remisePct ?? 0,
          quantiteStock: form.quantiteStock ?? 0,
          nombreOffresEnCours: 0
        }
      })
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Échec de la création.'
    } finally {
      isSubmitting.value = false
    }
  }

  function reset() {
    Object.assign(form, EMPTY)
    created.value = null
    error.value = null
  }

  return { form, isSubmitting, error, created, togglePrestation, submit, reset }
}


