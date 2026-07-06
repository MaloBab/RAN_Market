<script setup lang="ts">
import { ref } from 'vue'
import type { RobotMedia } from '@/types'

defineProps<{ media: RobotMedia }>()
const active = ref(0)
</script>

<template>
  <div class="space-y-2">
    <div class="aspect-[4/3] rounded-xl bg-ink-100 overflow-hidden border border-ink-200">
      <img :src="media.photosAvant[active]" class="w-full h-full object-cover" :alt="`Photo du robot, vue ${active + 1}`" />
    </div>
    <div v-if="media.photosAvant.length > 1" class="flex gap-2" role="tablist" aria-label="Photos du robot">
      <button
        v-for="(photo, i) in media.photosAvant" :key="i" @click="active = i"
        role="tab"
        :aria-selected="active === i"
        :aria-label="`Voir la photo ${i + 1} sur ${media.photosAvant.length}`"
        class="w-16 h-12 min-h-11 rounded-lg overflow-hidden border-2 transition-all duration-150 cursor-pointer"
        :class="active === i ? 'border-brand-red-600' : 'border-transparent opacity-60 hover:opacity-100'"
      >
        <img :src="photo" class="w-full h-full object-cover" alt="" />
      </button>
    </div>
  </div>
</template>
