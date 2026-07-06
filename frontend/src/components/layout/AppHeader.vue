<script setup lang="ts">
import { ref, watch } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth.store'
import ViewModeToggle from './ViewModeToggle.vue'
import { ScanSearch, LayoutGrid, Settings2, LogOut, Menu, X } from 'lucide-vue-next'

const auth = useAuthStore()
const router = useRouter()
const { currentUser, isCommercial, isResponsableRAN, isAuthenticated } = storeToRefs(auth)

const mobileOpen = ref(false)
watch(() => router.currentRoute.value.fullPath, () => { mobileOpen.value = false })

async function onLogout() {
  await auth.logout()
  router.push('/login')
}

const navLinkClass =
  'flex items-center gap-1.5 px-3 min-h-11 rounded-lg text-sm font-medium text-ink-500 hover:text-ink-900 hover:bg-ink-100 transition-colors'
const navLinkActiveClass = 'text-ink-900 bg-ink-100'
</script>

<template>
  <header class="sticky top-0 z-40 bg-white/90 backdrop-blur border-b border-ink-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-3">
      <RouterLink to="/" class="flex items-center gap-2.5 shrink-0">
        <span class="flex items-center justify-center w-9 h-9 rounded-lg bg-brand-yellow-500">
          <span class="font-heading font-extrabold text-[11px] text-brand-red-700 tracking-tight">FANUC</span>
        </span>
        <span class="font-heading font-bold text-lg text-ink-900 tracking-tight hidden xs:inline">Catalogue RAN</span>
      </RouterLink>

      <nav class="hidden md:flex items-center gap-1" aria-label="Navigation principale">
        <RouterLink to="/catalogue" :class="navLinkClass" :active-class="navLinkActiveClass">
          <ScanSearch class="size-4" aria-hidden="true" /> Catalogue
        </RouterLink>
        <RouterLink v-if="isCommercial" to="/coming-soon" :class="navLinkClass" :active-class="navLinkActiveClass">
          <LayoutGrid class="size-4" aria-hidden="true" /> Coming Soon
        </RouterLink>
        <RouterLink v-if="isResponsableRAN" to="/back-office" :class="navLinkClass" :active-class="navLinkActiveClass">
          <Settings2 class="size-4" aria-hidden="true" /> Back-office
        </RouterLink>
      </nav>

      <div class="flex items-center gap-2 sm:gap-3">
        <ViewModeToggle class="hidden sm:flex" />
        <template v-if="isAuthenticated">
          <div class="hidden lg:flex flex-col items-end leading-tight">
            <span class="text-sm font-medium text-ink-900">{{ currentUser?.nom }}</span>
            <span class="text-xs text-ink-500">{{ currentUser?.role }}</span>
          </div>
          <button
            @click="onLogout"
            class="hidden md:inline-flex p-2 rounded-lg text-ink-400 hover:text-brand-red-600 hover:bg-brand-red-100/60 transition-colors cursor-pointer"
            aria-label="Se déconnecter"
          >
            <LogOut class="size-4" aria-hidden="true" />
          </button>
        </template>
        <RouterLink v-else to="/login" class="hidden md:inline-flex text-sm font-medium text-ink-700 hover:text-ink-900">
          Connexion
        </RouterLink>

        <button
          class="md:hidden p-2 -mr-2 rounded-lg text-ink-700 hover:bg-ink-100 transition-colors cursor-pointer"
          :aria-expanded="mobileOpen"
          aria-controls="mobile-nav"
          :aria-label="mobileOpen ? 'Fermer le menu' : 'Ouvrir le menu'"
          @click="mobileOpen = !mobileOpen"
        >
          <component :is="mobileOpen ? X : Menu" class="size-5" aria-hidden="true" />
        </button>
      </div>
    </div>

    <Transition
      enter-active-class="transition-all duration-200 ease-[var(--ease-ran)]"
      enter-from-class="opacity-0 -translate-y-1"
      leave-active-class="transition-all duration-150"
      leave-to-class="opacity-0 -translate-y-1"
    >
      <nav
        v-if="mobileOpen"
        id="mobile-nav"
        aria-label="Navigation principale (mobile)"
        class="md:hidden border-t border-ink-200 bg-white px-4 py-3 flex flex-col gap-1"
      >
        <RouterLink to="/catalogue" :class="navLinkClass" :active-class="navLinkActiveClass">
          <ScanSearch class="size-4" aria-hidden="true" /> Catalogue
        </RouterLink>
        <RouterLink v-if="isCommercial" to="/coming-soon" :class="navLinkClass" :active-class="navLinkActiveClass">
          <LayoutGrid class="size-4" aria-hidden="true" /> Coming Soon
        </RouterLink>
        <RouterLink v-if="isResponsableRAN" to="/back-office" :class="navLinkClass" :active-class="navLinkActiveClass">
          <Settings2 class="size-4" aria-hidden="true" /> Back-office
        </RouterLink>

        <div class="flex items-center justify-between pt-2 mt-1 border-t border-ink-200">
          <ViewModeToggle />
          <button v-if="isAuthenticated" @click="onLogout" class="flex items-center gap-1.5 min-h-11 px-3 text-brand-red-600 font-medium cursor-pointer">
            <LogOut class="size-4" aria-hidden="true" /> Déconnexion
          </button>
          <RouterLink v-else to="/login" class="flex items-center min-h-11 px-3 text-ink-700 font-medium">Connexion</RouterLink>
        </div>
      </nav>
    </Transition>
  </header>
</template>
