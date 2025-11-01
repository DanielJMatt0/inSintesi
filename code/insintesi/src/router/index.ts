import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/views/Login.vue';
import Dashboard from '@/views/Dashboard.vue';
import TopicResponse from '@/views/TopicResponse.vue';
import ReportView from "@/views/ReportView.vue";

const routes = [
    { path: '/', name: 'Login', component: Login },
    { path: '/dashboard', name: 'Dashboard', component: Dashboard },
    { path: '/respond/:token', name: 'TopicResponse', component: TopicResponse },
    {
        path: "/report/:questionId",
        name: "report",
        component: ReportView,
        props: true,
    },
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