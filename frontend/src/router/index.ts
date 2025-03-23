import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/missions',
      name: 'missions',
      component: () => import('../views/MissionsView.vue')
    },
    {
      path: '/fleet',
      name: 'fleet',
      component: () => import('../views/FleetView.vue')
    }
  ]
})

export default router
