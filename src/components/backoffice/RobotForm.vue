<script setup lang="ts">
import { useRobotForm } from '@/composables/useRobotForm'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import type { BaieType, NiveauRenovation, RobotType } from '@/types'
import { CheckCircle2 } from 'lucide-vue-next'

const { form, isSubmitting, error, created, togglePrestation, submit, reset } = useRobotForm()

const TYPES: RobotType[] = ['Articulé', 'Soudure arc', 'Palettisation', 'Peinture', 'Delta', 'Collaboratif']
const BAIES: BaieType[] = ['R-30iB', 'R-30iB Plus', 'R-30iA']
const AXES = [4, 5, 6, 7] as const
const PRESTATIONS: NiveauRenovation[] = ['Peinture', 'Standard', 'Premium', 'Quasi Neuve', 'Extension de garantie', 'Échange standard']
</script>

<template>
  <div v-if="created" class="flex flex-col items-center text-center gap-3 py-10">
    <CheckCircle2 class="size-10 text-ran-ok-500" />
    <p class="font-display text-xl text-ran-graphite-100">Fiche créée en statut « Brouillon »</p>
    <p class="text-sm text-ran-graphite-400 font-mono">{{ created.id }} — {{ created.modele }}</p>
    <BaseButton variant="ghost" size="sm" @click="reset">Créer une autre fiche</BaseButton>
  </div>

  <form v-else @submit.prevent="submit" class="space-y-6">
    <fieldset class="space-y-3">
      <legend class="font-display text-lg text-ran-graphite-100 mb-1">Identification</legend>
      <div class="grid sm:grid-cols-2 gap-3">
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">ID Robot *</label>
          <BaseInput v-model="form.id" placeholder="FANUC-2026-001" />
        </div>
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Modèle *</label>
          <BaseInput v-model="form.modele" placeholder="ARC Mate 100iD" />
        </div>
      </div>
      <div class="grid sm:grid-cols-3 gap-3">
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Type *</label>
          <BaseSelect v-model="form.type" :options="TYPES.map(t => ({ value: t, label: t }))" placeholder="Sélectionner…" />
        </div>
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Catégorie</label>
          <BaseInput v-model="form.categorie" placeholder="Ex : Soudure" />
        </div>
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Année de service</label>
          <BaseInput type="number" :model-value="String(form.anneeMiseEnService ?? '')" @update:modelValue="v => form.anneeMiseEnService = v ? Number(v) : null" placeholder="2020" />
        </div>
      </div>
      <div>
        <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Description courte</label>
        <textarea v-model="form.descriptionCourte" rows="2" maxlength="300" class="w-full bg-ran-graphite-900 border border-ran-graphite-600 px-3 py-2 text-sm text-ran-graphite-100 placeholder:text-ran-graphite-400 focus:outline-none focus:border-ran-yellow-500 transition-colors" placeholder="Robot de soudure compact…" />
      </div>
    </fieldset>

    <fieldset class="space-y-3 border-t border-ran-graphite-700 pt-5">
      <legend class="font-display text-lg text-ran-graphite-100 mb-1">Caractéristiques techniques</legend>
      <div class="grid sm:grid-cols-3 gap-3">
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Payload (kg) *</label>
          <BaseInput type="number" :model-value="String(form.payloadKg ?? '')" @update:modelValue="v => form.payloadKg = v ? Number(v) : null" placeholder="12" />
        </div>
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Rayon d'action (mm) *</label>
          <BaseInput type="number" :model-value="String(form.rayonActionMm ?? '')" @update:modelValue="v => form.rayonActionMm = v ? Number(v) : null" placeholder="1441" />
        </div>
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Heures d'utilisation</label>
          <BaseInput type="number" :model-value="String(form.heuresUtilisation ?? '')" @update:modelValue="v => form.heuresUtilisation = v ? Number(v) : null" placeholder="14500" />
        </div>
      </div>
      <div class="grid sm:grid-cols-3 gap-3">
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Axes *</label>
          <div class="flex gap-1.5">
            <button
              v-for="a in AXES" :key="a" type="button" @click="form.axes = a"
              class="size-9 text-xs border transition-colors"
              :class="form.axes === a ? 'border-ran-yellow-500 text-ran-yellow-500 bg-ran-yellow-500/10' : 'border-ran-graphite-600 text-ran-graphite-300 hover:border-ran-steel-500'"
            >{{ a }}</button>
          </div>
        </div>
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Type de baie *</label>
          <BaseSelect v-model="form.typeBaie" :options="BAIES.map(b => ({ value: b, label: b }))" placeholder="Sélectionner…" />
        </div>
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Protection IP</label>
          <BaseInput v-model="form.protectionIp" placeholder="IP67" />
        </div>
      </div>
      <div>
        <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Montage</label>
        <BaseInput v-model="form.montage" placeholder="Sol / Plafond" />
      </div>
    </fieldset>

    <fieldset class="space-y-3 border-t border-ran-graphite-700 pt-5">
      <legend class="font-display text-lg text-ran-graphite-100 mb-1">Commercial &amp; stock</legend>
      <div class="grid sm:grid-cols-3 gap-3">
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Prix catalogue (€) *</label>
          <BaseInput type="number" :model-value="String(form.prixCatalogueEUR ?? '')" @update:modelValue="v => form.prixCatalogueEUR = v ? Number(v) : null" placeholder="28000" />
        </div>
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Remise (%)</label>
          <BaseInput type="number" :model-value="String(form.remisePct ?? '')" @update:modelValue="v => form.remisePct = v ? Number(v) : null" placeholder="20" />
        </div>
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Quantité en stock</label>
          <BaseInput type="number" :model-value="String(form.quantiteStock ?? '')" @update:modelValue="v => form.quantiteStock = v ? Number(v) : null" placeholder="3" />
        </div>
      </div>
    </fieldset>

    <fieldset class="space-y-3 border-t border-ran-graphite-700 pt-5">
      <legend class="font-display text-lg text-ran-graphite-100 mb-1">Prestations de rénovation disponibles</legend>
      <div class="flex flex-wrap gap-1.5">
        <button
          v-for="p in PRESTATIONS" :key="p" type="button" @click="togglePrestation(p)"
          class="px-2.5 py-1 text-xs border transition-colors"
          :class="form.prestations.includes(p) ? 'border-ran-yellow-500 text-ran-yellow-500 bg-ran-yellow-500/10' : 'border-ran-graphite-600 text-ran-graphite-300 hover:border-ran-steel-500'"
        >{{ p }}</button>
      </div>
      <p class="text-[11px] text-ran-graphite-500">Les photos sont ajoutées manuellement depuis la fiche après création.</p>
    </fieldset>

    <p v-if="error" class="text-sm text-ran-alert-500">{{ error }}</p>

    <BaseButton type="submit" class="w-full" :disabled="isSubmitting">
      {{ isSubmitting ? 'Création…' : 'Créer la fiche robot' }}
    </BaseButton>
  </form>
</template>
