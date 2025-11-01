import { createRouter, createWebHistory } from "vue-router";
import ReportView from "../views/ReportView.vue";

const routes = [
  {
    path: "/report/:questionId",
    name: "report",
    component: ReportView,
    props: true,
  },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
