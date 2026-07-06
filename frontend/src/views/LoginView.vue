<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import { Lock } from 'lucide-vue-next'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const form = reactive({ email: '', password: '' })

async function onSubmit() {
  const ok = await auth.login({ email: form.email, password: form.password })
  if (ok) {
    const redirect = (route.query.redirect as string) || '/catalogue'
    router.push(redirect)
  }
}
</script>

<template>
  <div class="min-h-[calc(100svh-4rem)] flex items-center justify-center px-6 py-10 bg-page">
    <BaseCard class="w-full max-w-sm p-8 space-y-6">
      <div class="flex flex-col items-center gap-3 text-center">
        <span class="flex items-center justify-center w-12 h-12 rounded-xl bg-brand-yellow-500">
          <span class="font-heading font-extrabold text-xs text-brand-red-700 tracking-tight">FANUC</span>
        </span>
        <div>
          <h1 class="font-heading font-bold text-xl text-ink-900">Catalogue RAN</h1>
          <p class="text-sm text-ink-500 mt-1">Connexion réservée aux équipes FANUC RAN</p>
        </div>
      </div>

      <form @submit.prevent="onSubmit" class="space-y-4" novalidate>
        <div>
          <label for="login-email" class="block text-xs font-medium text-ink-500 mb-1.5">Email</label>
          <BaseInput id="login-email" v-model="form.email" type="email" placeholder="prenom.nom@fanuc-ran.example" autocomplete="username" />
        </div>
        <div>
          <label for="login-password" class="block text-xs font-medium text-ink-500 mb-1.5">Mot de passe</label>
          <BaseInput id="login-password" v-model="form.password" type="password" placeholder="••••••••" autocomplete="current-password" />
        </div>

        <p v-if="auth.loginError" class="text-sm text-danger-600" role="alert">{{ auth.loginError }}</p>

        <BaseButton type="submit" class="w-full" :loading="auth.isLoggingIn" :disabled="auth.isLoggingIn">
          <Lock class="size-3.5" aria-hidden="true" />
          {{ auth.isLoggingIn ? 'Connexion…' : 'Se connecter' }}
        </BaseButton>
      </form>

      <div class="border-t border-ink-200 pt-4 text-xs text-ink-500 space-y-1">
        <p class="text-ink-700 font-medium mb-1">Comptes de démonstration :</p>
        <p class="font-mono">commercial@fanuc-ran.example / Commercial#2026</p>
        <p class="font-mono">responsable@fanuc-ran.example / ResponsableRAN#2026</p>
      </div>
    </BaseCard>
  </div>
</template>
