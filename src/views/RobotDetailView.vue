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
import { FileDown, ArrowLeft } from 'lucide-vue-next'

const route = useRoute()
const robot = ref<Robot | null>(null)
const notFound = ref(false)
const { fields, prixFinal } = useViewStrategy()

async function load() {
  const id = route.params.id as string
  const result = await robotService.getById(id)
  robot.value = result
  notFound.value = !result
}

onMounted(load)
watch(() => route.params.id, load)
</script>

<template>
  <div class="max-w-6xl mx-auto px-6 py-8">
    <RouterLink to="/catalogue" class="inline-flex items-center gap-1.5 text-xs font-mono uppercase tracking-wider text-ran-graphite-400 hover:text-ran-yellow-500 mb-6">
      <ArrowLeft class="size-3.5" /> Retour au catalogue
    </RouterLink>

    <div v-if="notFound" class="py-24 text-center text-ran-graphite-400">Fiche robot introuvable.</div>

    <div v-else-if="robot" class="grid lg:grid-cols-2 gap-10">
      <div class="space-y-6">
        <RobotGallery :media="robot.media" />
        <div v-if="robot.media.videoUrl" class="text-xs text-ran-steel-300 font-mono">▶ Vidéo de présentation disponible</div>
      </div>

      <div class="space-y-6">
        <div>
          <BaseBadge tone="yellow">{{ robot.type }}</BaseBadge>
          <h1 class="font-display text-4xl tracking-wide text-ran-graphite-100 mt-2">{{ robot.modele }}</h1>
          <p class="text-sm font-mono text-ran-graphite-400">{{ robot.id }} · Mis en service en {{ robot.anneeMiseEnService }}</p>
        </div>

        <p class="text-ran-graphite-300">{{ robot.descriptionCourte }}</p>

        <RobotCommercialPanel v-if="fields.showPrix" :robot="robot" :prix-final="prixFinal(robot)" />

        <div>
          <h2 class="font-display text-lg tracking-wide text-ran-graphite-100 mb-3">Caractéristiques techniques</h2>
          <RobotSpecsTable :robot="robot" />
        </div>

        <div>
          <h2 class="font-display text-lg tracking-wide text-ran-graphite-100 mb-3">Niveaux de rénovation disponibles</h2>
          <RenovationLevels :prestations="robot.prestationsDisponibles" />
        </div>

        <div v-if="robot.documentation.datasheetUrl || robot.documentation.flyerUrl || robot.documentation.brochureUrl" class="flex flex-wrap gap-2">
          <a v-if="robot.documentation.datasheetUrl" :href="robot.documentation.datasheetUrl" class="inline-flex items-center gap-1.5 text-xs font-mono text-ran-steel-300 hover:text-ran-yellow-500 border border-ran-graphite-600 px-3 py-1.5">
            <FileDown class="size-3.5" /> Datasheet
          </a>
          <a v-if="robot.documentation.flyerUrl" :href="robot.documentation.flyerUrl" class="inline-flex items-center gap-1.5 text-xs font-mono text-ran-steel-300 hover:text-ran-yellow-500 border border-ran-graphite-600 px-3 py-1.5">
            <FileDown class="size-3.5" /> Flyer
          </a>
          <a v-if="robot.documentation.brochureUrl" :href="robot.documentation.brochureUrl" class="inline-flex items-center gap-1.5 text-xs font-mono text-ran-steel-300 hover:text-ran-yellow-500 border border-ran-graphite-600 px-3 py-1.5">
            <FileDown class="size-3.5" /> Brochure
          </a>
        </div>

        <RouterLink :to="{ path: '/devis', query: { robotId: robot.id } }">
          <BaseButton class="w-full">Demander un devis pour ce robot</BaseButton>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
