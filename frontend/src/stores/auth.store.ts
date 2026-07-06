import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { AuthenticatedUser, AuthSession, Credentials, DisplayMode, UserRole } from '@/types'
import { authService } from '@/services'

const SESSION_STORAGE_KEY = 'ran-catalogue.session-token'

/**
 * Authentification réelle (login/session/logout) + mode d'affichage
 * actif (commerciale/client), qui n'est pertinent que pour un
 * Commercial authentifié (CDC §5.2).
 *
 * Le token est gardé en `sessionStorage` (effacé à la fermeture de
 * l'onglet) plutôt qu'en `localStorage`, pour limiter la durée de vie
 * du secret côté client. En production, ce token serait de toute façon
 * un cookie httpOnly + secure géré par le serveur, invisible du JS.
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
    sessionStorage.setItem(SESSION_STORAGE_KEY, session.token)
  }

  function clearSession() {
    currentUser.value = null
    sessionToken.value = null
    sessionStorage.removeItem(SESSION_STORAGE_KEY)
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
    if (sessionToken.value) {
      await authService.logout(sessionToken.value)
    }
    clearSession()
  }

  /** Revalide un token stocké au (re)chargement de l'app. */
  async function restoreSession() {
    isRestoring.value = true
    const token = sessionStorage.getItem(SESSION_STORAGE_KEY)
    if (!token) {
      isRestoring.value = false
      return
    }
    const session = await authService.getSession(token)
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


