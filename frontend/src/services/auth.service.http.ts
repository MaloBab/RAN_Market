import type { AuthService } from './api.contracts'
import type { AuthenticatedUser, AuthSession, Credentials } from '@/types'
import { apiFetch, setAccessToken } from './http'

/** Forme exacte de la réponse JSON de /auth/login et /auth/refresh (voir backend/src/auth/schemas.py::AccessTokenResponse). */
interface AccessTokenResponseDto {
  accessToken: string
  tokenType: string
  expiresIn: number // secondes
  user: AuthenticatedUser
}

function toSession(dto: AccessTokenResponseDto): AuthSession {
  setAccessToken(dto.accessToken)
  return {
    token: dto.accessToken,
    user: dto.user,
    expiresAt: Date.now() + dto.expiresIn * 1000
  }
}

class HttpAuthService implements AuthService {
  async login(credentials: Credentials): Promise<AuthSession> {
    const dto = await apiFetch<AccessTokenResponseDto>('/auth/login', {
      method: 'POST',
      body: credentials
    })
    return toSession(dto)
  }

  async logout(): Promise<void> {
    try {
      await apiFetch<void>('/auth/logout', { method: 'POST' })
    } finally {
      // On efface le token local même si l'appel réseau échoue (déconnexion
      // "optimiste" côté client) : pas de raison de garder l'utilisateur
      // bloqué en état connecté si le serveur est momentanément injoignable.
      setAccessToken(null)
    }
  }

  async refreshSession(): Promise<AuthSession | null> {
    try {
      const dto = await apiFetch<AccessTokenResponseDto>('/auth/refresh', {
        method: 'POST',
        isRetry: true // pas de refresh-sur-refresh si le cookie est absent/expiré
      })
      return toSession(dto)
    } catch {
      setAccessToken(null)
      return null
    }
  }
}

export const authService: AuthService = new HttpAuthService()