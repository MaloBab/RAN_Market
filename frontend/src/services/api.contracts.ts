/**
 * Interfaces de service (DIP) — chaque store/composable dépend de ces
 * abstractions, jamais des implémentations concrètes directement.
 *
 * NB sur AuthService : la signature a changé par rapport à la version mock.
 * Le backend réel gère le refresh token via un cookie httpOnly (jamais
 * exposé au JS), donc logout/refresh n'ont plus besoin qu'on leur passe un
 * token explicitement — le navigateur l'envoie automatiquement avec
 * `credentials: 'include'`.
 */
import type {
  AuthSession,
  CatalogueFilters,
  ComingSoonEntry,
  Credentials,
  DevisRequest,
  DevisSubmissionResult,
  ImportReport,
  Robot
} from '@/types'

export interface AuthService {
  /** POST /auth/login — Body: Credentials → access token + user (cookie refresh posé par le serveur). */
  login(credentials: Credentials): Promise<AuthSession>

  /** POST /auth/logout — révoque le refresh token courant (lu depuis le cookie httpOnly) et l'efface. */
  logout(): Promise<void>

  /**
   * POST /auth/refresh — utilise le cookie httpOnly pour émettre un nouvel
   * access token, sans réauthentification. Renvoie `null` si aucune session
   * active (pas de cookie, ou refresh token expiré/révoqué).
   */
  refreshSession(): Promise<AuthSession | null>
}

export interface RobotService {
  /** GET /robots?... — catalogue filtré (vue client ou commerciale selon l'auth). */
  list(filters: Partial<CatalogueFilters>): Promise<Robot[]>

  /** GET /robots/:id — renvoie `null` si absente ou non publiée (404 backend). */
  getById(id: string): Promise<Robot | null>

  /** GET /coming-soon — réservé vue commerciale (401/403 backend sinon). */
  listComingSoon(): Promise<ComingSoonEntry[]>

  /** POST /robots (back-office, rôle responsable_ran requis). Statut initial "Brouillon". */
  create(input: Omit<Robot, 'statut'>): Promise<Robot>
}

export interface DevisService {
  /** POST /devis — Body: DevisRequest. Réponse: référence + commercial assigné. */
  submit(payload: DevisRequest): Promise<DevisSubmissionResult>
}

export interface ImportService {
  /** POST /imports/robots (multipart/form-data, champ `file`) → ImportReport. */
  importExcel(file: File, onProgress?: (pct: number) => void): Promise<ImportReport>
}