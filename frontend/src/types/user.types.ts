/**
 * Profils utilisateurs (CDC §2). Le rôle pilote l'accès (router guards)
 * et, pour le Commercial, le mode d'affichage actif (Strategy, voir
 * composables/useViewStrategy.ts).
 */

export type UserRole = 'commercial' | 'client' | 'responsable_ran'

export interface AuthenticatedUser {
  id: string
  nom: string
  email: string
  role: UserRole
}

/** Mode d'affichage actif côté Commercial — bascule via le toggle (§5.2). */
export type DisplayMode = 'commerciale' | 'client'

/** Session active — token opaque + expiration, jamais le mot de passe. */
export interface AuthSession {
  token: string
  user: AuthenticatedUser
  expiresAt: number // epoch ms
}

export interface Credentials {
  email: string
  password: string
}


