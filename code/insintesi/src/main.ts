// src/main.ts
import { createApp } from "vue";
import { createPinia } from 'pinia';
import App from "./App.vue";
import router from "@/router";
import "./assets/main.css";

// Crea l'app Vue e usa il router
const app = createApp(App);
app.use(createPinia());
app.use(router);
app.mount("#app");
