/**
 * Client HTTP central — point de passage unique de tous les appels au
 * backend FastAPI.
 *
 * L'access token est gardé en mémoire dans ce module (pas de
 * sessionStorage/localStorage) : il ne survit pas à un rechargement de
 * page, mais `restoreSession()` (voir auth.store.ts) le régénère au boot
 * de l'app via /auth/refresh, en s'appuyant sur le cookie httpOnly. C'est
 * la pratique recommandée pour un JWT d'accès (surface d'exposition XSS
 * minimale), le cookie httpOnly reste la seule chose qui persiste.
 */

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

export class ApiError extends Error {
  readonly status: number

  constructor(status: number, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

let accessToken: string | null = null

export function setAccessToken(token: string | null): void {
  accessToken = token
}

export function getAccessToken(): string | null {
  return accessToken
}

interface RequestOptions extends Omit<RequestInit, 'body'> {
  body?: unknown
  /** Usage interne : évite de retenter un refresh à l'infini. */
  isRetry?: boolean
}

async function extractErrorMessage(response: Response): Promise<string> {
  try {
    const data = await response.json()
    if (typeof data?.detail === 'string') return data.detail
    if (Array.isArray(data?.detail)) {
      // Erreurs de validation Pydantic : [{ loc, msg, type }, ...]
      return data.detail.map((err: { msg?: string }) => err.msg).filter(Boolean).join(' ')
    }
  } catch {
    // Corps non-JSON ou vide : on retombe sur le message générique ci-dessous.
  }
  return `Erreur ${response.status}`
}

let refreshInFlight: Promise<boolean> | null = null

/** Rafraîchit l'access token via le cookie httpOnly. Mutualise les appels concurrents. */
async function refreshAccessToken(): Promise<boolean> {
  if (!refreshInFlight) {
    refreshInFlight = (async () => {
      try {
        const response = await fetch(`${BASE_URL}/auth/refresh`, {
          method: 'POST',
          credentials: 'include'
        })
        if (!response.ok) {
          setAccessToken(null)
          return false
        }
        const data = await response.json()
        setAccessToken(data.accessToken)
        return true
      } catch {
        setAccessToken(null)
        return false
      } finally {
        refreshInFlight = null
      }
    })()
  }
  return refreshInFlight
}

export async function apiFetch<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { body, isRetry, headers, ...rest } = options
  const isFormData = body instanceof FormData

  const finalHeaders: Record<string, string> = {
    Accept: 'application/json',
    ...(!isFormData && body !== undefined ? { 'Content-Type': 'application/json' } : {}),
    ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
    ...(headers as Record<string, string> | undefined)
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    ...rest,
    credentials: 'include',
    headers: finalHeaders,
    body: body === undefined ? undefined : isFormData ? (body as FormData) : JSON.stringify(body)
  })

  // Refresh silencieux à la première expiration rencontrée, jamais sur
  // /auth/login (identifiants invalides = vraie erreur, pas un token expiré)
  // ni en boucle sur une requête déjà retentée.
  if (response.status === 401 && !isRetry && path !== '/auth/login') {
    const refreshed = await refreshAccessToken()
    if (refreshed) {
      return apiFetch<T>(path, { ...options, isRetry: true })
    }
  }

  if (!response.ok) {
    throw new ApiError(response.status, await extractErrorMessage(response))
  }

  if (response.status === 204) {
    return undefined as T
  }

  return (await response.json()) as T
}