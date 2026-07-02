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
  <div v-if="lastResult" class="flex flex-col items-center text-center gap-3 py-10">
    <CheckCircle2 class="size-10 text-ran-ok-500" />
    <p class="font-display text-xl text-ran-graphite-100">Demande envoyée</p>
    <p class="text-sm text-ran-graphite-400">
      Référence <span class="font-mono text-ran-yellow-500">{{ lastResult.reference }}</span><br />
      Prise en charge par {{ lastResult.commercialAssigne }}
    </p>
  </div>

  <form v-else @submit.prevent="onSubmit" class="space-y-4">
    <p v-if="robotId" class="text-xs font-mono text-ran-steel-300">Robot pré-sélectionné : {{ robotId }}</p>

    <div class="grid sm:grid-cols-2 gap-3">
      <div>
        <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Prénom</label>
        <BaseInput v-model="form.prenom" placeholder="Prénom" />
      </div>
      <div>
        <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Nom</label>
        <BaseInput v-model="form.nom" placeholder="Nom" />
      </div>
    </div>

    <div class="grid sm:grid-cols-2 gap-3">
      <div>
        <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Email</label>
        <BaseInput v-model="form.email" type="email" placeholder="vous@societe.com" />
      </div>
      <div>
        <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Téléphone</label>
        <BaseInput v-model="form.telephone" type="tel" placeholder="+33 6 …" />
      </div>
    </div>

    <div class="grid sm:grid-cols-3 gap-3">
      <div>
        <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Pays</label>
        <BaseInput v-model="form.pays" placeholder="France" />
      </div>
      <div>
        <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Société</label>
        <BaseInput v-model="form.societe!" placeholder="Société" />
      </div>
      <div>
        <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Fonction</label>
        <BaseInput v-model="form.fonction!" placeholder="Fonction" />
      </div>
    </div>

    <div v-if="prestationsDisponibles?.length">
      <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1.5">Prestations souhaitées</label>
      <div class="flex flex-wrap gap-1.5">
        <button
          v-for="p in prestationsDisponibles" :key="p" type="button" @click="togglePrestation(p)"
          class="px-2.5 py-1 text-xs border transition-colors"
          :class="form.prestationsSouhaitees.includes(p) ? 'border-ran-yellow-500 text-ran-yellow-500 bg-ran-yellow-500/10' : 'border-ran-graphite-600 text-ran-graphite-300 hover:border-ran-steel-500'"
        >{{ p }}</button>
      </div>
    </div>

    <div>
      <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Demande spéciale</label>
      <textarea v-model="form.demandeSpeciale" rows="3" class="w-full bg-ran-graphite-900 border border-ran-graphite-600 px-3 py-2 text-sm text-ran-graphite-100 placeholder:text-ran-graphite-400 focus:outline-none focus:border-ran-yellow-500 transition-colors" placeholder="Précisions, contraintes, délais…" />
    </div>

    <p v-if="error" class="text-sm text-ran-alert-500">{{ error }}</p>

    <BaseButton type="submit" class="w-full" :disabled="isSubmitting">
      {{ isSubmitting ? 'Envoi…' : 'Envoyer la demande de devis' }}
    </BaseButton>
  </form>
</template>
