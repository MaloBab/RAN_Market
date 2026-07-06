<script setup lang="ts">
defineProps<{
  modelValue: string
  options: { value: string; label: string }[]
  placeholder?: string
  id?: string
  disabled?: boolean
}>()
defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<template>
  <select
    :id="id"
    :value="modelValue"
    :disabled="disabled"
    @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
    class="w-full min-h-11 bg-white rounded-lg border border-ink-200 px-3.5 py-2.5 text-sm text-ink-900 transition-colors duration-150 focus:outline-none focus:border-brand-red-600 focus:ring-2 focus:ring-brand-red-600/15 disabled:bg-ink-50 disabled:cursor-not-allowed cursor-pointer"
  >
    <option value="">{{ placeholder ?? 'Tous' }}</option>
    <option v-for="opt in options" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
  </select>
</template>
