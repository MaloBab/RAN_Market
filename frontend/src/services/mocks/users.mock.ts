/**
 * "Pseudo base de données" d'utilisateurs — en dur, en attendant un
 * vrai backend (annuaire d'entreprise / SSO FANUC). Aucun mot de passe
 * en clair : seuls le sel et le hash PBKDF2-SHA256 sont stockés, générés
 * hors-ligne (voir script de génération dans la doc du projet).
 *
 * Comptes de démonstration :
 *   commercial@fanuc-ran.example   / Commercial#2026
 *   responsable@fanuc-ran.example  / ResponsableRAN#2026
 */
import type { AuthenticatedUser } from '@/types'

export interface StoredUser {
  user: AuthenticatedUser
  saltHex: string
  passwordHashHex: string
}

export const MOCK_USERS: StoredUser[] = [
  {
    user: {
      id: 'usr-001',
      nom: 'Camille Berthier',
      email: 'commercial@fanuc-ran.example',
      role: 'commercial'
    },
    saltHex: '41871a0c18aa31153da902b8e8ee3e90',
    passwordHashHex: '8655fc482a119690967258a573d21733a82ba1b0479b749def2f4e6f460f4279'
  },
  {
    user: {
      id: 'usr-002',
      nom: 'Julien Ferreira',
      email: 'responsable@fanuc-ran.example',
      role: 'responsable_ran'
    },
    saltHex: '8ada16f4c9d26e7e058d87d13679aba3',
    passwordHashHex: 'd48949a49d43cfad3a75273a4c4552d5020adfc8106378dcd6e658df6fa7fb8d'
  }
]


