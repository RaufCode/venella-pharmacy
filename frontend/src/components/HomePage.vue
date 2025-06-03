<script setup>
    import Header from "./customer/Header.vue";
    import Main from "./customer/Main.vue";
    import Footer from "./customer/Footer.vue";

    import { useAuthStore } from "@/stores/auth"; // adjust path if needed
    const authStore = useAuthStore();
</script>

<template>
    <div>
        <Header />
        <Main />
        <Footer />
    </div>
</template>
