<script setup lang="ts">
/**
 * Élément signature de l'UI : matérialise visuellement le masquage
 * d'une donnée commerciale en Vue Client (au lieu d'un simple v-if qui
 * ferait disparaître l'info sans trace, on montre une zone "redacted"
 * façon dossier confidentiel — renforce pédagogiquement la séparation
 * des vues pour le commercial qui fait la démo).
 */
defineProps<{ visible: boolean; width?: string }>()
</script>

<template>
  <span v-if="visible"><slot /></span>
  <span v-else class="ran-redacted inline-block py-0.5 px-2" :style="{ width: width ?? '6rem' }">••••</span>
</template>


