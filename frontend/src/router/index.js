import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignUpView from '../views/SignUpView.vue'
import SignInView from '../views/SignInView.vue'
import DashboardView from '../views/DashboardView.vue'
import CartsView from '../views/CartsView.vue'
import OrdersView from '../views/OrdersView.vue'
import ProductDetailsView from '../views/ProductDetailsView.vue'
import SalesPersonView from '../views/SalesPersonView.vue'
import CheckoutView from '../views/CheckOutView.vue'
import { useAuthStore } from '@/stores/auth'

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
      meta: { requiresAuth: true, requiresRole: 'admin' },
    },
    {
      path: '/carts',
      name: 'carts',
      component: CartsView,
      meta: { requiresAuth: true },
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: CheckoutView,
      meta: { requiresAuth: true },
    },
    {
      path: '/orders',
      name: 'orders',
      component: OrdersView,
      meta: { requiresAuth: true },
    },
    {
      path: '/details',
      name: 'product-details',
      component: ProductDetailsView,
    },
    {
      path: '/salesperson',
      name: 'salesperson',
      component: SalesPersonView,
      meta: { requiresAuth: true, requiresRole: 'admin' },
    },
  ],
})

// Route guard with authentication and role check
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()

  // Ensure the auth store is initialized
  if (!auth.ready) {
    await auth.initializeAuth()
  }

  const isAuthRequired = to.meta.requiresAuth
  const requiredRole = to.meta.requiresRole
  const isAuthenticated = auth.isAuthenticated
  const userRole = auth.user?.role

  if (isAuthRequired && !isAuthenticated) {
    return next('/login')
  }

  if (requiredRole && userRole !== requiredRole) {
    return next('/') // or show a 403 page if desired
  }

  next()
})

export default router
