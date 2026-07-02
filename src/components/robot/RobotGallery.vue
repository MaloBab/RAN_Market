<script setup lang="ts">
import { ref } from 'vue'
import type { RobotMedia } from '@/types'

defineProps<{ media: RobotMedia }>()
const active = ref(0)
</script>

<template>
  <div class="space-y-2">
    <div class="ran-bracket aspect-[4/3] bg-ran-graphite-800 overflow-hidden">
      <img :src="media.photosAvant[active]" class="w-full h-full object-cover" alt="Photo du robot" />
    </div>
    <div v-if="media.photosAvant.length > 1" class="flex gap-2">
      <button
        v-for="(photo, i) in media.photosAvant" :key="i" @click="active = i"
        class="w-16 h-12 overflow-hidden border-2 transition-colors"
        :class="active === i ? 'border-ran-yellow-500' : 'border-transparent opacity-60 hover:opacity-100'"
      >
        <img :src="photo" class="w-full h-full object-cover" alt="" />
      </button>
    </div>
  </div>
</template>
