<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <a href="#main-content" class="skip-link">Aller au contenu principal</a>
    <AppHeader />
    <main id="main-content" class="flex-1">
      <RouterView v-slot="{ Component }">
        <Transition name="ran-page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>
  </div>
</template>
