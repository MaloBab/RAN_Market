import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { AuthenticatedUser, AuthSession, Credentials, DisplayMode, UserRole } from '@/types'
import { authService } from '@/services'

/**
 * Authentification réelle (login/session/logout) + mode d'affichage
 * actif (commerciale/client), qui n'est pertinent que pour un
 * Commercial authentifié (CDC §5.2).
 */
export const useAuthStore = defineStore('auth', () => {
  const currentUser = ref<AuthenticatedUser | null>(null)
  const sessionToken = ref<string | null>(null)
  const displayMode = ref<DisplayMode>('commerciale')
  const isRestoring = ref(true)
  const loginError = ref<string | null>(null)
  const isLoggingIn = ref(false)

  const isAuthenticated = computed(() => currentUser.value !== null)
  const role = computed<UserRole | null>(() => currentUser.value?.role ?? null)
  const isCommercial = computed(() => role.value === 'commercial')
  const isResponsableRAN = computed(() => role.value === 'responsable_ran')
  const canToggleView = computed(() => isCommercial.value)

  const effectiveDisplayMode = computed<DisplayMode>(() =>
    isCommercial.value ? displayMode.value : 'client'
  )

  function applySession(session: AuthSession) {
    currentUser.value = session.user
    sessionToken.value = session.token
    displayMode.value = 'commerciale'
  }

  function clearSession() {
    currentUser.value = null
    sessionToken.value = null
  }

  async function login(credentials: Credentials): Promise<boolean> {
    isLoggingIn.value = true
    loginError.value = null
    try {
      const session = await authService.login(credentials)
      applySession(session)
      return true
    } catch (e) {
      loginError.value = e instanceof Error ? e.message : 'Échec de la connexion.'
      return false
    } finally {
      isLoggingIn.value = false
    }
  }

  async function logout() {
    await authService.logout()
    clearSession()
  }

  /**
   * Au (re)chargement de l'app : tente un refresh silencieux via le cookie
   * httpOnly. Si aucune session active côté serveur (pas de cookie, ou
   * refresh token expiré/révoqué), l'utilisateur reste simplement déconnecté
   * — pas d'erreur affichée, c'est un état normal (première visite, etc.).
   */
  async function restoreSession() {
    isRestoring.value = true
    const session = await authService.refreshSession()
    if (session) {
      applySession(session)
    } else {
      clearSession()
    }
    isRestoring.value = false
  }

  function toggleDisplayMode() {
    if (!canToggleView.value) return
    displayMode.value = displayMode.value === 'commerciale' ? 'client' : 'commerciale'
  }

  return {
    currentUser, role, isAuthenticated, isCommercial, isResponsableRAN,
    canToggleView, displayMode, effectiveDisplayMode, isRestoring,
    loginError, isLoggingIn,
    login, logout, restoreSession, toggleDisplayMode
  }
})