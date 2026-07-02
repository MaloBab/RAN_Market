import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/catalogue' },
    { path: '/login', name: 'login', component: () => import('@/views/LoginView.vue'), meta: { public: true } },
    { path: '/catalogue', name: 'catalogue', component: () => import('@/views/CatalogueView.vue') },
    { path: '/robot/:id', name: 'robot-detail', component: () => import('@/views/RobotDetailView.vue') },
    { path: '/comparateur', name: 'comparateur', component: () => import('@/views/CompareView.vue'), meta: { requiresCommercial: true } },
    { path: '/coming-soon', name: 'coming-soon', component: () => import('@/views/ComingSoonView.vue'), meta: { requiresCommercial: true } },
    { path: '/devis', name: 'devis', component: () => import('@/views/DevisView.vue'), meta: { public: true } },
    { path: '/back-office', name: 'back-office', component: () => import('@/views/BackOfficeView.vue'), meta: { requiresRAN: true } },
    { path: '/back-office/nouveau', name: 'back-office-nouveau', component: () => import('@/views/BackOfficeNewRobotView.vue'), meta: { requiresRAN: true } }
  ]
})

/**
 * Garde de navigation — authentification + séparation stricte des
 * droits par rôle (CDC §4.3). La vue Client (/devis, fiches robots)
 * reste accessible sans compte (lien partagé), le reste exige une
 * session valide.
 */
router.beforeEach(async (to) => {
  const auth = useAuthStore()

  if (auth.isRestoring) {
    await auth.restoreSession()
  }

  const isPublic = to.meta.public === true || to.name === 'robot-detail' || to.name === 'catalogue'
  if (!isPublic && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.requiresCommercial && !auth.isCommercial) return '/catalogue'
  if (to.meta.requiresRAN && !auth.isResponsableRAN) return '/catalogue'
  if (to.name === 'login' && auth.isAuthenticated) return '/catalogue'

  return true
})

export default router
