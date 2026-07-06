<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import type { Robot } from '@/types'
import { robotService } from '@/services'
import { useViewStrategy } from '@/composables/useViewStrategy'
import RobotGallery from '@/components/robot/RobotGallery.vue'
import RobotSpecsTable from '@/components/robot/RobotSpecsTable.vue'
import RobotCommercialPanel from '@/components/robot/RobotCommercialPanel.vue'
import RenovationLevels from '@/components/robot/RenovationLevels.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import { FileDown, ArrowLeft, PlayCircle } from 'lucide-vue-next'

const route = useRoute()
const robot = ref<Robot | null>(null)
const isLoading = ref(true)
const notFound = ref(false)
const { fields, prixFinal } = useViewStrategy()

async function load() {
  isLoading.value = true
  const id = route.params.id as string
  const result = await robotService.getById(id)
  robot.value = result
  notFound.value = !result
  isLoading.value = false
}

onMounted(load)
watch(() => route.params.id, load)
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
    <RouterLink
      to="/catalogue"
      class="inline-flex items-center gap-1.5 min-h-9 text-sm font-medium text-ink-500 hover:text-ink-900 mb-6 transition-colors"
    >
      <ArrowLeft class="size-3.5" aria-hidden="true" /> Retour au catalogue
    </RouterLink>

    <div v-if="isLoading" class="grid lg:grid-cols-2 gap-10 animate-pulse" aria-hidden="true">
      <div class="aspect-[4/3] rounded-xl bg-white border border-ink-200" />
      <div class="space-y-4">
        <div class="h-8 w-2/3 rounded-lg bg-white border border-ink-200" />
        <div class="h-4 w-full rounded bg-white border border-ink-200" />
        <div class="h-32 w-full rounded-xl bg-white border border-ink-200" />
      </div>
    </div>

    <div v-else-if="notFound" class="py-24 text-center text-ink-500">
      <p class="font-heading font-semibold text-2xl text-ink-900 mb-2">Fiche robot introuvable</p>
      <p class="text-sm mb-6">Ce robot n'existe plus ou a été retiré du catalogue.</p>
      <RouterLink to="/catalogue"><BaseButton variant="secondary">Retour au catalogue</BaseButton></RouterLink>
    </div>

    <div v-else-if="robot" class="grid lg:grid-cols-2 gap-8 lg:gap-10">
      <div class="space-y-3 lg:sticky lg:top-20 lg:self-start">
        <RobotGallery :media="robot.media" />
        <div v-if="robot.media.videoUrl" class="flex items-center gap-1.5 text-xs font-medium text-ink-500">
          <PlayCircle class="size-3.5" aria-hidden="true" /> Vidéo de présentation disponible
        </div>
      </div>

      <div class="space-y-6">
        <div>
          <BaseBadge tone="yellow">{{ robot.type }}</BaseBadge>
          <h1 class="font-heading font-extrabold text-3xl sm:text-4xl tracking-tight text-ink-900 mt-2">{{ robot.modele }}</h1>
          <p class="text-sm text-ink-500 font-mono">{{ robot.id }} · Mis en service en {{ robot.anneeMiseEnService }}</p>
        </div>

        <p class="text-ink-700 leading-relaxed">{{ robot.descriptionCourte }}</p>

        <RobotCommercialPanel v-if="fields.showPrix" :robot="robot" :prix-final="prixFinal(robot)" />

        <div>
          <h2 class="font-heading font-semibold text-lg text-ink-900 mb-3">Caractéristiques techniques</h2>
          <RobotSpecsTable :robot="robot" />
        </div>

        <div>
          <h2 class="font-heading font-semibold text-lg text-ink-900 mb-3">Niveaux de rénovation disponibles</h2>
          <RenovationLevels :prestations="robot.prestationsDisponibles" />
        </div>

        <div v-if="robot.documentation.datasheetUrl || robot.documentation.flyerUrl || robot.documentation.brochureUrl" class="flex flex-wrap gap-2">
          <a
            v-if="robot.documentation.datasheetUrl" :href="robot.documentation.datasheetUrl"
            class="inline-flex items-center gap-1.5 min-h-10 text-xs font-medium text-ink-600 hover:text-brand-red-600 hover:border-ink-300 rounded-lg border border-ink-200 px-3 transition-colors"
          >
            <FileDown class="size-3.5" aria-hidden="true" /> Datasheet
          </a>
          <a
            v-if="robot.documentation.flyerUrl" :href="robot.documentation.flyerUrl"
            class="inline-flex items-center gap-1.5 min-h-10 text-xs font-medium text-ink-600 hover:text-brand-red-600 hover:border-ink-300 rounded-lg border border-ink-200 px-3 transition-colors"
          >
            <FileDown class="size-3.5" aria-hidden="true" /> Flyer
          </a>
          <a
            v-if="robot.documentation.brochureUrl" :href="robot.documentation.brochureUrl"
            class="inline-flex items-center gap-1.5 min-h-10 text-xs font-medium text-ink-600 hover:text-brand-red-600 hover:border-ink-300 rounded-lg border border-ink-200 px-3 transition-colors"
          >
            <FileDown class="size-3.5" aria-hidden="true" /> Brochure
          </a>
        </div>

        <RouterLink :to="{ path: '/devis', query: { robotId: robot.id } }">
          <BaseButton size="lg" class="w-full">Demander un devis pour ce robot</BaseButton>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
