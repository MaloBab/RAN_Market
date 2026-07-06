<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  modelValue: string
  placeholder?: string
  type?: string
  id?: string
  error?: string
  disabled?: boolean
  autocomplete?: string
}>()
defineEmits<{ 'update:modelValue': [value: string] }>()

const errorId = computed(() => (props.id ? `${props.id}-error` : undefined))
</script>

<template>
  <div>
    <input
      :id="id"
      :type="type ?? 'text'"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :autocomplete="autocomplete"
      :aria-invalid="!!error"
      :aria-describedby="error ? errorId : undefined"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      class="w-full min-h-11 bg-white rounded-lg border px-3.5 py-2.5 text-sm text-ink-900 placeholder:text-ink-400 transition-colors duration-150 focus:outline-none focus:border-brand-red-600 focus:ring-2 focus:ring-brand-red-600/15 disabled:bg-ink-50 disabled:cursor-not-allowed"
      :class="error ? 'border-danger-600' : 'border-ink-200'"
    />
    <p v-if="error" :id="errorId" class="mt-1.5 text-xs text-danger-600">{{ error }}</p>
  </div>
</template>
