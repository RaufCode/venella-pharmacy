import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignUpView from '../views/SignUpView.vue'
import SignInView from '../views/SignInView.vue'
import DashboardView from '../views/DashboardView.vue'
import CustomerDashboardView from '../views/CustomerDashboardView.vue'
import { useAuthStore } from '@/stores/auth' // Adjust the path as needed
import { createPinia } from 'pinia'

const pinia = createPinia() // Required if you're using Pinia outside setup
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/register',
      name: 'register',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'login',
      component: SignInView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
    },
    {
      path: '/customer-dashboard',
      name: 'customer-dashboard',
      component: CustomerDashboardView,
      meta: { requiresAuth: true },
    },
  ],
})

// Route guard
router.beforeEach((to, from, next) => {
  const auth = useAuthStore(pinia)
  const isAuthenticated = auth.isAuthenticated

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
