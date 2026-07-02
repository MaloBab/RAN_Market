<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth.store'
import ViewModeToggle from './ViewModeToggle.vue'
import { Boxes, ScanSearch, LayoutGrid, Settings2, LogOut } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const { currentUser, isCommercial, isResponsableRAN, isAuthenticated } = storeToRefs(auth)

async function onLogout() {
  await auth.logout()
  router.push('/login')
}
</script>

<template>
  <header class="sticky top-0 z-40 bg-ran-graphite-950/95 backdrop-blur border-b border-ran-graphite-700">
    <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
      <RouterLink to="/" class="flex items-center gap-2.5">
        <Boxes class="size-5 text-ran-yellow-500" />
        <span class="font-display text-2xl tracking-wide leading-none">
          CATALOGUE <span class="text-ran-yellow-500">RAN</span>
        </span>
      </RouterLink>

      <nav class="hidden md:flex items-center gap-1 font-mono text-xs uppercase tracking-wider">
        <RouterLink to="/catalogue" class="flex items-center gap-1.5 px-3 py-2 text-ran-graphite-300 hover:text-ran-yellow-500 transition-colors">
          <ScanSearch class="size-3.5" /> Catalogue
        </RouterLink>
        <RouterLink v-if="isCommercial" to="/coming-soon" class="flex items-center gap-1.5 px-3 py-2 text-ran-graphite-300 hover:text-ran-yellow-500 transition-colors">
          <LayoutGrid class="size-3.5" /> Coming Soon
        </RouterLink>
        <RouterLink v-if="isResponsableRAN" to="/back-office" class="flex items-center gap-1.5 px-3 py-2 text-ran-graphite-300 hover:text-ran-yellow-500 transition-colors">
          <Settings2 class="size-3.5" /> Back-office
        </RouterLink>
      </nav>

      <div class="flex items-center gap-4">
        <ViewModeToggle />
        <template v-if="isAuthenticated">
          <div class="hidden sm:flex flex-col items-end leading-tight">
            <span class="text-xs text-ran-graphite-100">{{ currentUser?.nom }}</span>
            <span class="text-[10px] font-mono uppercase text-ran-graphite-400">{{ currentUser?.role }}</span>
          </div>
          <button @click="onLogout" class="text-ran-graphite-400 hover:text-ran-alert-500 transition-colors" title="Se déconnecter">
            <LogOut class="size-4" />
          </button>
        </template>
        <RouterLink v-else to="/login" class="text-xs font-mono uppercase tracking-wider text-ran-graphite-300 hover:text-ran-yellow-500">
          Connexion
        </RouterLink>
      </div>
    </div>
  </header>
</template>
