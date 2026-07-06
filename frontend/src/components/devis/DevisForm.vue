<script setup lang="ts">
import { useDevisForm } from '@/composables/useDevisForm'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import type { NiveauRenovation } from '@/types'
import { CheckCircle2 } from 'lucide-vue-next'

const props = defineProps<{ robotId?: string; prestationsDisponibles?: NiveauRenovation[] }>()
const { form, togglePrestation, submit, isSubmitting, lastResult, error } = useDevisForm(props.robotId)

async function onSubmit() {
  try {
    await submit()
  } catch {
    // erreur affichée via `error`
  }
}
</script>

<template>
  <div v-if="lastResult" class="flex flex-col items-center text-center gap-3 py-10" role="status">
    <CheckCircle2 class="size-10 text-ok-600" aria-hidden="true" />
    <p class="font-heading font-semibold text-xl text-ink-900">Demande envoyée</p>
    <p class="text-sm text-ink-500">
      Référence <span class="font-mono font-semibold text-ink-900">{{ lastResult.reference }}</span><br />
      Prise en charge par {{ lastResult.commercialAssigne }}
    </p>
  </div>

  <form v-else @submit.prevent="onSubmit" class="space-y-4" novalidate>
    <p v-if="robotId" class="text-xs text-ink-500 bg-ink-100 rounded-lg px-3 py-2 inline-block">Robot pré-sélectionné : {{ robotId }}</p>

    <div class="grid sm:grid-cols-2 gap-3">
      <div>
        <label for="devis-prenom" class="block text-xs font-medium text-ink-500 mb-1.5">Prénom</label>
        <BaseInput id="devis-prenom" v-model="form.prenom" placeholder="Prénom" autocomplete="given-name" />
      </div>
      <div>
        <label for="devis-nom" class="block text-xs font-medium text-ink-500 mb-1.5">Nom</label>
        <BaseInput id="devis-nom" v-model="form.nom" placeholder="Nom" autocomplete="family-name" />
      </div>
    </div>

    <div class="grid sm:grid-cols-2 gap-3">
      <div>
        <label for="devis-email" class="block text-xs font-medium text-ink-500 mb-1.5">Email</label>
        <BaseInput id="devis-email" v-model="form.email" type="email" placeholder="vous@societe.com" autocomplete="email" />
      </div>
      <div>
        <label for="devis-tel" class="block text-xs font-medium text-ink-500 mb-1.5">Téléphone</label>
        <BaseInput id="devis-tel" v-model="form.telephone" type="tel" placeholder="+33 6 …" autocomplete="tel" />
      </div>
    </div>

    <div class="grid sm:grid-cols-3 gap-3">
      <div>
        <label for="devis-pays" class="block text-xs font-medium text-ink-500 mb-1.5">Pays</label>
        <BaseInput id="devis-pays" v-model="form.pays" placeholder="France" autocomplete="country-name" />
      </div>
      <div>
        <label for="devis-societe" class="block text-xs font-medium text-ink-500 mb-1.5">Société</label>
        <BaseInput id="devis-societe" v-model="form.societe!" placeholder="Société" autocomplete="organization" />
      </div>
      <div>
        <label for="devis-fonction" class="block text-xs font-medium text-ink-500 mb-1.5">Fonction</label>
        <BaseInput id="devis-fonction" v-model="form.fonction!" placeholder="Fonction" autocomplete="organization-title" />
      </div>
    </div>

    <div v-if="prestationsDisponibles?.length" role="group" aria-labelledby="devis-prestations-label">
      <span id="devis-prestations-label" class="block text-xs font-medium text-ink-500 mb-1.5">Prestations souhaitées</span>
      <div class="flex flex-wrap gap-1.5">
        <button
          v-for="p in prestationsDisponibles" :key="p" type="button" @click="togglePrestation(p)"
          class="px-2.5 min-h-9 rounded-full text-xs font-medium border transition-colors cursor-pointer"
          :class="form.prestationsSouhaitees.includes(p) ? 'border-brand-red-600 text-brand-red-600 bg-brand-red-100/60' : 'border-ink-200 text-ink-600 hover:border-ink-300 hover:bg-ink-50'"
          :aria-pressed="form.prestationsSouhaitees.includes(p)"
        >{{ p }}</button>
      </div>
    </div>

    <div>
      <label for="devis-message" class="block text-xs font-medium text-ink-500 mb-1.5">Demande spéciale</label>
      <textarea
        id="devis-message"
        v-model="form.demandeSpeciale"
        rows="3"
        class="w-full bg-white rounded-lg border border-ink-200 px-3.5 py-2.5 text-sm text-ink-900 placeholder:text-ink-400 transition-colors duration-150 focus:outline-none focus:border-brand-red-600 focus:ring-2 focus:ring-brand-red-600/15"
        placeholder="Précisions, contraintes, délais…"
      />
    </div>

    <p v-if="error" class="text-sm text-danger-600" role="alert">{{ error }}</p>

    <BaseButton type="submit" class="w-full" :loading="isSubmitting" :disabled="isSubmitting">
      {{ isSubmitting ? 'Envoi…' : 'Envoyer la demande de devis' }}
    </BaseButton>
  </form>
</template>
