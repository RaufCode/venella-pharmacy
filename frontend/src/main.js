import '../src/styles.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import axios from 'axios';
import App from './App.vue';
import router from './router';
import { useAuthStore } from './stores/auth';
axios.defaults.baseURL = "https://techrems.pythonanywhere.com";

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

app.mount('#app');

// ✅ Initialize auth AFTER app is mounted and Pinia is available
const authStore = useAuthStore();
authStore.initializeAuth();
