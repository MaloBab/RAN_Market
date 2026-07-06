/**
 * Interfaces de service (DIP) — chaque store/composable dépend de ces
 * abstractions, jamais des implémentations mock directement. Le jour où
 * un vrai backend existe, on écrit une classe `HttpXxxService implements
 * XxxService` et on la branche dans `services/index.ts` sans toucher au
 * reste de l'app.
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
  /**
   * POST /api/auth/login  Body: Credentials  → AuthSession
   * Backend réel : vérifie le hash (bcrypt/argon2) côté serveur, émet
   * un JWT signé + refresh token en cookie httpOnly. Ce mock vérifie un
   * hash PBKDF2 local à titre de démonstration — ce n'est PAS un
   * mécanisme de sécurité de production (voir utils/crypto.ts).
   */
  login(credentials: Credentials): Promise<AuthSession>

  /** POST /api/auth/logout — invalide le token côté serveur. */
  logout(token: string): Promise<void>

  /** GET /api/auth/session — revalide un token existant (ex: au reload). */
  getSession(token: string): Promise<AuthSession | null>
}

export interface RobotService {
  /**
   * GET /api/robots?filters=...
   * Retourne le catalogue filtré. Le filtrage est fait côté service
   * (mock: en mémoire) pour refléter un futur filtrage côté serveur.
   */
  list(filters: Partial<CatalogueFilters>): Promise<Robot[]>

  /** GET /api/robots/:id */
  getById(id: string): Promise<Robot | null>

  /** GET /api/coming-soon — réservé vue commerciale (filtré côté serveur). */
  listComingSoon(): Promise<ComingSoonEntry[]>

  /**
   * POST /api/robots  (back-office, rôle responsable_ran requis)
   * Création manuelle d'une fiche robot (CDC §2.3). Statut initial
   * "Brouillon" comme pour l'import Excel, jusqu'à validation.
   */
  create(input: Omit<Robot, 'statut'>): Promise<Robot>
}

export interface DevisService {
  /**
   * POST /api/devis
   * Body: DevisRequest. Réponse: référence + commercial assigné.
   * Le backend réel enverrait l'email via le provider SMTP/SendGrid
   * mentionné au CDC §4.4.
   */
  submit(payload: DevisRequest): Promise<DevisSubmissionResult>
}

export interface ImportService {
  /**
   * POST /api/back-office/import (multipart/form-data, champ `file`)
   * Réponse: ImportReport. En attendant un vrai backend, le mock simule
   * un parsing ligne à ligne avec une progression observable.
   */
  importExcel(
    file: File,
    onProgress?: (pct: number) => void
  ): Promise<ImportReport>
}


