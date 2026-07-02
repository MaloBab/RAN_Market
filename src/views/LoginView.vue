<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import { Boxes, Lock } from 'lucide-vue-next'

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
  <div class="min-h-screen flex items-center justify-center px-6">
    <BaseCard bracket class="w-full max-w-sm p-8 space-y-6">
      <div class="flex flex-col items-center gap-2 text-center">
        <Boxes class="size-7 text-ran-yellow-500" />
        <h1 class="font-display text-2xl tracking-wide text-ran-graphite-100">CATALOGUE RAN</h1>
        <p class="text-xs text-ran-graphite-400">Connexion réservée aux équipes FANUC RAN</p>
      </div>

      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Email</label>
          <BaseInput v-model="form.email" type="email" placeholder="prenom.nom@fanuc-ran.example" />
        </div>
        <div>
          <label class="block text-[11px] font-mono uppercase tracking-wider text-ran-graphite-400 mb-1">Mot de passe</label>
          <BaseInput v-model="form.password" type="password" placeholder="••••••••" />
        </div>

        <p v-if="auth.loginError" class="text-sm text-ran-alert-500">{{ auth.loginError }}</p>

        <BaseButton type="submit" class="w-full" :disabled="auth.isLoggingIn">
          <Lock class="size-3.5" />
          {{ auth.isLoggingIn ? 'Connexion…' : 'Se connecter' }}
        </BaseButton>
      </form>

      <div class="border-t border-ran-graphite-700 pt-4 text-[11px] font-mono text-ran-graphite-500 space-y-1">
        <p class="text-ran-graphite-400 mb-1">Comptes de démonstration :</p>
        <p>commercial@fanuc-ran.example / Commercial#2026</p>
        <p>responsable@fanuc-ran.example / ResponsableRAN#2026</p>
      </div>
    </BaseCard>
  </div>
</template>
