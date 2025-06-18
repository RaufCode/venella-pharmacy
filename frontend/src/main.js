import '../src/styles.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import axios from 'axios';
import App from './App.vue';
import router from './router';
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";


axios.defaults.baseURL = "https://techrems.pythonanywhere.com";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(Toast);

// Restore auth token and axios header on app start
import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();
authStore.initializeAuth();

app.mount('#app');

