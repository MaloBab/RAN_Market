import type { ImportService } from './api.contracts'
import type { ImportReport } from '@/types'
import { getAccessToken } from './http'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

/**
 * `fetch` ne fournit pas d'événement de progression sur l'upload (seulement
 * sur la lecture de la réponse) — on utilise donc XMLHttpRequest pour cette
 * seule route, afin de garder la barre de progression du back-office
 * fonctionnelle avec un vrai backend.
 */
class HttpImportService implements ImportService {
  importExcel(file: File, onProgress?: (pct: number) => void): Promise<ImportReport> {
    return new Promise((resolve, reject) => {
      const formData = new FormData()
      formData.append('file', file)

      const xhr = new XMLHttpRequest()
      xhr.open('POST', `${BASE_URL}/imports/robots`)
      xhr.withCredentials = true // transmet le cookie httpOnly, comme fetch avec credentials: 'include'

      const token = getAccessToken()
      if (token) xhr.setRequestHeader('Authorization', `Bearer ${token}`)

      xhr.upload.addEventListener('progress', (event) => {
        if (event.lengthComputable) {
          onProgress?.(Math.round((event.loaded / event.total) * 100))
        }
      })

      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            resolve(JSON.parse(xhr.responseText) as ImportReport)
          } catch {
            reject(new Error('Réponse serveur invalide.'))
          }
          return
        }
        // Le refresh automatique sur 401 (géré ailleurs pour les requêtes
        // JSON classiques) n'est pas répliqué ici par simplicité : un import
        // Excel est une action ponctuelle et explicite, l'utilisateur peut
        // relancer sans perte après une reconnexion si le token a expiré.
        try {
          const data = JSON.parse(xhr.responseText)
          reject(new Error(typeof data?.detail === 'string' ? data.detail : `Erreur ${xhr.status}`))
        } catch {
          reject(new Error(`Erreur ${xhr.status}`))
        }
      })

      xhr.addEventListener('error', () => reject(new Error("Échec réseau lors de l'import.")))
      xhr.send(formData)
    })
  }
}

export const importService: ImportService = new HttpImportService()