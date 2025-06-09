<script setup>
    import { ref, computed, onUnmounted, watch } from "vue";
    import { useRoute, useRouter } from "vue-router";
    import { useOrderStore } from "@/stores/orderStore";

    import OverView from "./OverView.vue";
    import MedicationHero from "./MedicationHero.vue";
    import OrdersHero from "./OrdersHero.vue";
    import SalesHero from "./SalesHero.vue";
    import Notifications from "./Notifications.vue"; // Add this if not already

    import {
        Menu,
        X,
        Home,
        ShieldCheck,
        ShoppingCart,
        FileText,
        Bell,
        LogOut,
    } from "lucide-vue-next";

    const route = useRoute();
    const router = useRouter();
    const orderStore = useOrderStore();

    const activeTab = ref(route.query.tab || "overview");
    const hamburger = ref(false);

    // Notification count (replace this with dynamic value if needed)
    const notificationCount = ref(3);

    watch(
        () => route.query.tab,
        (newTab) => {
            if (newTab) activeTab.value = newTab;
        }
    );

    const tabLabel = computed(() => {
        switch (activeTab.value) {
            case "overview":
                return "Overview";
            case "medication":
                return "Medicines Hub";
            case "orders":
                return "Orders Hub";
            case "sales":
                return "Sales Hub";
            case "notifications":
                return "Notifications Hub";
            default:
                return "Vanella Pharmacy";
        }
    });

    let pollingInterval;
    onUnmounted(() => {
        clearInterval(pollingInterval);
    });

    function navigate(tabKey) {
        activeTab.value = tabKey;
        hamburger.value = false;
        router.push({ query: { tab: tabKey } });
    }
</script>

<template>
    <div class="pt-9 md:pt-0 md:flex h-screen w-screen">
        <!-- Top Bar (Mobile) -->
        <header>
            <div
                class="fixed top-0 md:hidden p-3 text-sm flex items-center justify-between bg-white shadow-md z-40 w-full"
            >
                <button
                    @click="hamburger = !hamburger"
                    aria-label="Open sidebar"
                >
                    <Menu class="w-5 h-5" />
                </button>
                <h1 class="text-2xl font-styleScript text-orange-600">
                    {{ tabLabel }}
                </h1>
                <RouterLink
                    to="/login"
                    aria-label="Logout"
                    class="text-gray-700"
                >
                    <LogOut class="w-5 h-5" />
                </RouterLink>
            </div>

            <!-- Overlay (Mobile) -->
            <div
                v-if="hamburger"
                @click="hamburger = false"
                class="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
            ></div>

            <!-- Sidebar -->
            <aside
                :class="[
                    'fixed md:static top-0 z-50 w-4/5 md:w-[220px] lg:w-[250px] bg-gray-50 h-screen text-gray-800 transition-all duration-500 ease-in-out transform',
                    hamburger
                        ? 'translate-x-0 opacity-100 blur-none'
                        : '-translate-x-full opacity-20 blur-sm pointer-events-none',
                    'md:translate-x-0 md:opacity-100 md:blur-none md:pointer-events-auto md:block',
                ]"
                aria-label="Sidebar"
            >
                <div class="pt-2 flex items-center gap-4 justify-end md:block">
                    <h1
                        class="font-styleScript text-2xl text-center py-2 md:py-6 text-orange-600 md:text-3xl"
                    >
                        Dashboard
                    </h1>
                    <button
                        @click="hamburger = !hamburger"
                        class="pr-2 md:hidden"
                        aria-label="Close sidebar"
                    >
                        <X class="w-5 h-5" />
                    </button>
                </div>

                <!-- Navigation -->
                <nav class="md:flex flex-col">
                    <button
                        @click="navigate('overview')"
                        class="a-dashboard-navs"
                        :class="{
                            'bg-orange-600 text-white hover:bg-orange-500':
                                activeTab === 'overview',
                        }"
                    >
                        <Home class="w-5 h-5 mr-2" /> Overview
                    </button>

                    <button
                        @click="navigate('medication')"
                        class="a-dashboard-navs"
                        :class="{
                            'bg-orange-600 text-white hover:bg-orange-500':
                                activeTab === 'medication',
                        }"
                    >
                        <ShieldCheck class="w-5 h-5 mr-2" /> Medications
                    </button>

                    <button
                        @click="navigate('orders')"
                        class="a-dashboard-navs"
                        :class="{
                            'bg-orange-600 text-white hover:bg-orange-500':
                                activeTab === 'orders',
                        }"
                    >
                        <ShoppingCart class="w-5 h-5 mr-2" /> Orders
                    </button>

                    <button
                        @click="navigate('sales')"
                        class="a-dashboard-navs"
                        :class="{
                            'bg-orange-600 text-white hover:bg-orange-500':
                                activeTab === 'sales',
                        }"
                    >
                        <FileText class="w-5 h-5 mr-2" /> Sales
                    </button>

                    <button
                        @click="navigate('notifications')"
                        class="a-dashboard-navs relative"
                        :class="{
                            'bg-orange-600 text-white hover:bg-orange-500':
                                activeTab === 'notifications',
                        }"
                    >
                        <Bell class="w-5 h-5 mr-2" />
                        Notifications

                        <!-- Notification badge -->
                        <span
                            v-if="notificationCount > 0"
                            class="absolute top-0 right-[95px] md:right-12 lg:right-20 bg-red-600 text-white text-xs px-1.5 py-0.5 rounded-full"
                        >
                            {{ notificationCount }}
                        </span>
                    </button>

                    <RouterLink to="/login" class="block mt-16 md:mt-20">
                        <button
                            class="py-2 w-full pl-3 rounded font-medium text-sm flex items-center gap-4 text-gray-800 md:pl-5 hover:bg-gray-100 focus:bg-orange-600 focus:text-white"
                        >
                            <LogOut class="w-5 h-5" /> Logout
                        </button>
                    </RouterLink>
                </nav>
            </aside>
        </header>

        <!-- Main Content -->
        <main class="w-full h-screen overflow-auto">
            <div class="mx-auto">
                <OverView v-if="activeTab === 'overview'" />
                <MedicationHero v-if="activeTab === 'medication'" />
                <OrdersHero v-if="activeTab === 'orders'" />
                <SalesHero v-if="activeTab === 'sales'" />
                <Notifications v-if="activeTab === 'notifications'" />
            </div>
        </main>
    </div>
</template>

<style scoped>
    /* Add any custom styles if needed */
</style>
