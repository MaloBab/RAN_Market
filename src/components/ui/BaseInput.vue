<script setup lang="ts">
defineProps<{ modelValue: string; placeholder?: string; type?: string }>()
defineEmits<{ 'update:modelValue': [value: string] }>()
</script>

<template>
  <input
    :type="type ?? 'text'"
    :value="modelValue"
    :placeholder="placeholder"
    @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    class="w-full bg-ran-graphite-900 border border-ran-graphite-600 px-3 py-2 text-sm text-ran-graphite-100 placeholder:text-ran-graphite-400 focus:outline-none focus:border-ran-yellow-500 transition-colors"
  />
</template>
