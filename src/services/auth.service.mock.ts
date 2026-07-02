import type { AuthService } from './api.contracts'
import type { AuthSession, Credentials } from '@/types'
import { MOCK_USERS } from './mocks/users.mock'
import { hashPassword, timingSafeEqual, randomToken } from '@/utils/crypto'
import { delay } from './delay'

const SESSION_TTL_MS = 8 * 60 * 60 * 1000 // 8h, aligné sur une journée de travail

/** Table de sessions en mémoire — équivalent mock d'un store Redis côté serveur. */
const activeSessions = new Map<string, AuthSession>()

class MockAuthService implements AuthService {
  async login({ email, password }: Credentials): Promise<AuthSession> {
    await delay(300)

    const record = MOCK_USERS.find((u) => u.user.email.toLowerCase() === email.trim().toLowerCase())

    // Toujours dériver le hash même si l'utilisateur n'existe pas, pour ne
    // pas laisser une différence de timing révéler si l'email est connu.
    const candidateHash = await hashPassword(password, record?.saltHex ?? MOCK_USERS[0]!.saltHex)

    if (!record || !timingSafeEqual(candidateHash, record.passwordHashHex)) {
      throw new Error('Identifiants incorrects.')
    }

    const session: AuthSession = {
      token: randomToken(),
      user: record.user,
      expiresAt: Date.now() + SESSION_TTL_MS
    }
    activeSessions.set(session.token, session)
    return session
  }

  async logout(token: string): Promise<void> {
    await delay(120)
    activeSessions.delete(token)
  }

  async getSession(token: string): Promise<AuthSession | null> {
    await delay(80)
    const session = activeSessions.get(token)
    if (!session) return null
    if (session.expiresAt < Date.now()) {
      activeSessions.delete(token)
      return null
    }
    return session
  }
}

export const authService: AuthService = new MockAuthService()
