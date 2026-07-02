<script setup lang="ts">
defineProps<{ modelValue: string; options: { value: string; label: string }[]; placeholder?: string }>()
defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<template>
  <select
    :value="modelValue"
    @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
    class="w-full bg-ran-graphite-900 border border-ran-graphite-600 px-3 py-2 text-sm text-ran-graphite-100 focus:outline-none focus:border-ran-yellow-500 transition-colors"
  >
    <option value="">{{ placeholder ?? 'Tous' }}</option>
    <option v-for="opt in options" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
  </select>
</template>
