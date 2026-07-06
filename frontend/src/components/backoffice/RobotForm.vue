<script setup lang="ts">
import { useRobotForm } from '@/composables/useRobotForm'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import type { BaieType, NiveauRenovation, RobotType } from '@/types'
import { CheckCircle2 } from 'lucide-vue-next'

const { form, isSubmitting, error, created, togglePrestation, submit, reset } = useRobotForm()

const TYPES: RobotType[] = ['Articulé', 'Soudure arc', 'Palettisation', 'Peinture', 'Delta', 'Collaboratif']
const BAIES: BaieType[] = ['R-30iB', 'R-30iB Plus', 'R-30iA']
const AXES = [4, 5, 6, 7] as const
const PRESTATIONS: NiveauRenovation[] = ['Peinture', 'Standard', 'Premium', 'Quasi Neuve', 'Extension de garantie', 'Échange standard']

const labelClass = 'block text-xs font-medium text-ink-500 mb-1.5'
</script>

<template>
  <BaseCard v-if="created" class="flex flex-col items-center text-center gap-3 py-10 px-6">
    <CheckCircle2 class="size-10 text-ok-600" aria-hidden="true" />
    <p class="font-heading font-semibold text-xl text-ink-900">Fiche créée en statut « Brouillon »</p>
    <p class="text-sm text-ink-500 font-mono">{{ created.id }} — {{ created.modele }}</p>
    <BaseButton variant="ghost" size="sm" @click="reset">Créer une autre fiche</BaseButton>
  </BaseCard>

  <form v-else @submit.prevent="submit" class="space-y-6">
    <BaseCard class="p-5 space-y-4">
      <h2 class="font-heading font-semibold text-lg text-ink-900">Identification</h2>
      <div class="grid sm:grid-cols-2 gap-3">
        <div>
          <label for="rf-id" :class="labelClass">ID Robot *</label>
          <BaseInput id="rf-id" v-model="form.id" placeholder="FANUC-2026-001" />
        </div>
        <div>
          <label for="rf-modele" :class="labelClass">Modèle *</label>
          <BaseInput id="rf-modele" v-model="form.modele" placeholder="ARC Mate 100iD" />
        </div>
      </div>
      <div class="grid sm:grid-cols-3 gap-3">
        <div>
          <label for="rf-type" :class="labelClass">Type *</label>
          <BaseSelect id="rf-type" v-model="form.type" :options="TYPES.map(t => ({ value: t, label: t }))" placeholder="Sélectionner…" />
        </div>
        <div>
          <label for="rf-categorie" :class="labelClass">Catégorie</label>
          <BaseInput id="rf-categorie" v-model="form.categorie" placeholder="Ex : Soudure" />
        </div>
        <div>
          <label for="rf-annee" :class="labelClass">Année de service</label>
          <BaseInput id="rf-annee" type="number" :model-value="String(form.anneeMiseEnService ?? '')" @update:modelValue="v => form.anneeMiseEnService = v ? Number(v) : null" placeholder="2020" />
        </div>
      </div>
      <div>
        <label for="rf-description" :class="labelClass">Description courte</label>
        <textarea
          id="rf-description" v-model="form.descriptionCourte" rows="2" maxlength="300"
          class="w-full bg-white rounded-lg border border-ink-200 px-3.5 py-2.5 text-sm text-ink-900 placeholder:text-ink-400 focus:outline-none focus:border-brand-red-600 focus:ring-2 focus:ring-brand-red-600/15 transition-colors"
          placeholder="Robot de soudure compact…"
        />
      </div>
    </BaseCard>

    <BaseCard class="p-5 space-y-4">
      <h2 class="font-heading font-semibold text-lg text-ink-900">Caractéristiques techniques</h2>
      <div class="grid sm:grid-cols-3 gap-3">
        <div>
          <label for="rf-payload" :class="labelClass">Payload (kg) *</label>
          <BaseInput id="rf-payload" type="number" :model-value="String(form.payloadKg ?? '')" @update:modelValue="v => form.payloadKg = v ? Number(v) : null" placeholder="12" />
        </div>
        <div>
          <label for="rf-rayon" :class="labelClass">Rayon d'action (mm) *</label>
          <BaseInput id="rf-rayon" type="number" :model-value="String(form.rayonActionMm ?? '')" @update:modelValue="v => form.rayonActionMm = v ? Number(v) : null" placeholder="1441" />
        </div>
        <div>
          <label for="rf-heures" :class="labelClass">Heures d'utilisation</label>
          <BaseInput id="rf-heures" type="number" :model-value="String(form.heuresUtilisation ?? '')" @update:modelValue="v => form.heuresUtilisation = v ? Number(v) : null" placeholder="14500" />
        </div>
      </div>
      <div class="grid sm:grid-cols-3 gap-3">
        <div>
          <span id="rf-axes-label" :class="labelClass">Axes *</span>
          <div class="flex gap-1.5" role="group" aria-labelledby="rf-axes-label">
            <button
              v-for="a in AXES" :key="a" type="button" @click="form.axes = a"
              class="size-11 rounded-lg text-xs font-medium border transition-colors cursor-pointer"
              :class="form.axes === a ? 'border-brand-red-600 text-brand-red-600 bg-brand-red-100/60' : 'border-ink-200 text-ink-600 hover:border-ink-300 hover:bg-ink-50'"
              :aria-pressed="form.axes === a"
            >{{ a }}</button>
          </div>
        </div>
        <div>
          <label for="rf-baie" :class="labelClass">Type de baie *</label>
          <BaseSelect id="rf-baie" v-model="form.typeBaie" :options="BAIES.map(b => ({ value: b, label: b }))" placeholder="Sélectionner…" />
        </div>
        <div>
          <label for="rf-ip" :class="labelClass">Protection IP</label>
          <BaseInput id="rf-ip" v-model="form.protectionIp" placeholder="IP67" />
        </div>
      </div>
      <div>
        <label for="rf-montage" :class="labelClass">Montage</label>
        <BaseInput id="rf-montage" v-model="form.montage" placeholder="Sol / Plafond" />
      </div>
    </BaseCard>

    <BaseCard class="p-5 space-y-4">
      <h2 class="font-heading font-semibold text-lg text-ink-900">Commercial &amp; stock</h2>
      <div class="grid sm:grid-cols-3 gap-3">
        <div>
          <label for="rf-prix" :class="labelClass">Prix catalogue (€) *</label>
          <BaseInput id="rf-prix" type="number" :model-value="String(form.prixCatalogueEUR ?? '')" @update:modelValue="v => form.prixCatalogueEUR = v ? Number(v) : null" placeholder="28000" />
        </div>
        <div>
          <label for="rf-remise" :class="labelClass">Remise (%)</label>
          <BaseInput id="rf-remise" type="number" :model-value="String(form.remisePct ?? '')" @update:modelValue="v => form.remisePct = v ? Number(v) : null" placeholder="20" />
        </div>
        <div>
          <label for="rf-stock" :class="labelClass">Quantité en stock</label>
          <BaseInput id="rf-stock" type="number" :model-value="String(form.quantiteStock ?? '')" @update:modelValue="v => form.quantiteStock = v ? Number(v) : null" placeholder="3" />
        </div>
      </div>
    </BaseCard>

    <BaseCard class="p-5 space-y-3">
      <h2 class="font-heading font-semibold text-lg text-ink-900">Prestations de rénovation disponibles</h2>
      <div class="flex flex-wrap gap-1.5" role="group" aria-label="Prestations de rénovation disponibles">
        <button
          v-for="p in PRESTATIONS" :key="p" type="button" @click="togglePrestation(p)"
          class="px-2.5 min-h-9 rounded-full text-xs font-medium border transition-colors cursor-pointer"
          :class="form.prestations.includes(p) ? 'border-brand-red-600 text-brand-red-600 bg-brand-red-100/60' : 'border-ink-200 text-ink-600 hover:border-ink-300 hover:bg-ink-50'"
          :aria-pressed="form.prestations.includes(p)"
        >{{ p }}</button>
      </div>
      <p class="text-xs text-ink-500">Les photos sont ajoutées manuellement depuis la fiche après création.</p>
    </BaseCard>

    <p v-if="error" class="text-sm text-danger-600" role="alert">{{ error }}</p>

    <BaseButton type="submit" size="lg" class="w-full" :loading="isSubmitting" :disabled="isSubmitting">
      {{ isSubmitting ? 'Création…' : 'Créer la fiche robot' }}
    </BaseButton>
  </form>
</template>
