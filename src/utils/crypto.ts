/**
 * Hachage de mots de passe via Web Crypto (PBKDF2-SHA256, 100k itérations).
 * Aucune dépendance externe, aucun mot de passe en clair ni en mémoire
 * au-delà du temps de vérification.
 *
 * ⚠️ Limite inhérente à un frontend "pseudo-DB" : le sel + hash sont
 * livrés dans le bundle JS, donc visibles par quiconque inspecte le
 * code. Pour une vraie sécurité, cette vérification DOIT être déportée
 * côté serveur (jamais de comparaison de mot de passe côté client en
 * production) — voir le commentaire dans auth.service.mock.ts.
 */

const ITERATIONS = 100_000

async function deriveBits(password: string, salt: Uint8Array): Promise<ArrayBuffer> {
  const enc = new TextEncoder()
  const keyMaterial = await crypto.subtle.importKey('raw', enc.encode(password), 'PBKDF2', false, ['deriveBits'])
  return crypto.subtle.deriveBits(
    { name: 'PBKDF2', salt: salt as BufferSource, iterations: ITERATIONS, hash: 'SHA-256' },
    keyMaterial,
    256
  )
}

function toHex(buffer: ArrayBuffer): string {
  return Array.from(new Uint8Array(buffer)).map((b) => b.toString(16).padStart(2, '0')).join('')
}

function fromHex(hex: string): Uint8Array {
  const bytes = new Uint8Array(hex.length / 2)
  for (let i = 0; i < bytes.length; i++) bytes[i] = parseInt(hex.substr(i * 2, 2), 16)
  return bytes
}

export async function hashPassword(password: string, saltHex: string): Promise<string> {
  const bits = await deriveBits(password, fromHex(saltHex))
  return toHex(bits)
}

/** Comparaison en temps constant pour limiter les attaques par timing. */
export function timingSafeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false
  let diff = 0
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i)
  return diff === 0
}

export function randomToken(): string {
  return toHex(crypto.getRandomValues(new Uint8Array(32)).buffer)
}
