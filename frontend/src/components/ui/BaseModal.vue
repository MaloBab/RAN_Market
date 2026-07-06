<script setup lang="ts">
import { watch } from 'vue'
import { X } from 'lucide-vue-next'

const props = defineProps<{ open: boolean; title?: string }>()
const emit = defineEmits<{ close: [] }>()

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') emit('close')
}

watch(
  () => props.open,
  (open) => { document.body.style.overflow = open ? 'hidden' : '' }
)
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-150"
      enter-from-class="opacity-0"
      leave-active-class="transition-opacity duration-150"
      leave-to-class="opacity-0"
    >
      <div
        v-if="open"
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink-900/40 backdrop-blur-[2px]"
        @click.self="emit('close')"
        @keydown="onKeydown"
      >
        <Transition
          enter-active-class="transition-all duration-200 ease-[var(--ease-ran)]"
          enter-from-class="opacity-0 translate-y-2 scale-[0.98]"
          appear
        >
          <div
            role="dialog"
            aria-modal="true"
            :aria-labelledby="title ? 'base-modal-title' : undefined"
            class="w-full max-w-2xl max-h-[85vh] overflow-y-auto bg-surface rounded-2xl border border-ink-200 shadow-[var(--shadow-popover)]"
          >
            <div class="flex items-center justify-between px-5 py-4 border-b border-ink-200">
              <h2 id="base-modal-title" class="font-heading font-semibold text-lg text-ink-900">{{ title }}</h2>
              <button
                class="p-1.5 -mr-1.5 rounded-lg text-ink-400 hover:text-ink-900 hover:bg-ink-100 transition-colors cursor-pointer"
                @click="emit('close')"
                aria-label="Fermer la fenêtre"
              >
                <X class="size-5" />
              </button>
            </div>
            <div class="p-5"><slot /></div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>
