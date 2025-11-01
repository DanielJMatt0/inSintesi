import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/views/TokenAccessView.vue';
import Dashboard from '@/views/Dashboard.vue';
import ReportView from "@/views/ReportView.vue";
import TokenAccessView from '../views/TokenAccessView.vue';
import RespondView from '../views/RespondView.vue';
import RespondSuccessView from '../views/RespondSuccessView.vue';

const routes = [
    { path: '/', name: 'TokenAccess', component: TokenAccessView },
    { path: '/dashboard', name: 'Dashboard', component: Dashboard },
    { path: '/respond/:token', name: 'Respond', component: RespondView },
    { path: '/respond/success', name: 'RespondSuccess', component: RespondSuccessView },
    { path: "/report/:questionId", name: "report", component: ReportView, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

router.beforeEach((to, from, next) => {
    const adminAuth = localStorage.getItem('adminAuth')
    const isRespondPage = to.path.startsWith('/respond')
    const isLoginPage = to.path === '/'

    // User responding to a topic → always allowed
    if (isRespondPage) return next()

    // Not logged in and trying to access admin area
    if (!adminAuth && !isLoginPage) return next('/')

    // Logged in and trying to access login page
    if (adminAuth && isLoginPage) return next('/dashboard')

    next()
});