import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/views/TokenAccessView.vue';
import Dashboard from '@/views/Dashboard.vue';
import ReportView from "@/views/ReportView.vue";
import TokenAccessView from '../views/TokenAccessView.vue';
import RespondView from '../views/RespondView.vue';
import RespondSuccessView from '../views/RespondSuccessView.vue';
import LoginView from '../views/LoginView.vue';
import { useAuthStore } from "@/stores/authStore"

const routes = [
    { path: '/', name: 'TokenAccess', component: TokenAccessView },
    { path: '/dashboard', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
    { path: '/respond/:token', name: 'Respond', component: RespondView },
    { path: '/respond/success', name: 'RespondSuccess', component: RespondSuccessView },
    { path: "/report/:questionId", name: "Report", component: ReportView, props: true, meta: { requiresAuth: true } },
    { path: "/login", name: "Login", component: LoginView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

router.beforeEach((to, _from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    // if user not logged, redirect to home
    next({ name: "TokenAccess" })
  } else {
    next()
  }
})