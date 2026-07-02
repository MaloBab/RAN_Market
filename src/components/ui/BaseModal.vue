<script setup lang="ts">
defineProps<{ open: boolean; title?: string }>()
const emit = defineEmits<{ close: [] }>()
</script>

<template>
  <Teleport to="body">
    <Transition enter-active-class="transition-opacity duration-150" enter-from-class="opacity-0" leave-active-class="transition-opacity duration-150" leave-to-class="opacity-0">
      <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70" @click.self="emit('close')">
        <Transition enter-active-class="transition-all duration-200" enter-from-class="opacity-0 translate-y-2" appear>
          <div class="w-full max-w-2xl max-h-[85vh] overflow-y-auto bg-ran-graphite-900 border border-ran-graphite-600">
            <div class="flex items-center justify-between px-5 py-4 border-b border-ran-graphite-700">
              <h2 class="font-display text-xl tracking-wide text-ran-graphite-100">{{ title }}</h2>
              <button class="text-ran-graphite-400 hover:text-ran-yellow-500 text-xl leading-none" @click="emit('close')" aria-label="Fermer">×</button>
            </div>
            <div class="p-5"><slot /></div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>
