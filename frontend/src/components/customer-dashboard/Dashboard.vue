<script setup>
    import { ref, computed } from "vue";
    import HomeHero from "./HomeHero.vue";
    import MedicationHero from "./MedicationHero.vue";

    const activeTab = ref("home");
    const hamburger = ref(false);

    // Label for the top bar
    const tabLabel = computed(() => {
        switch (activeTab.value) {
            case "home":
                return "home";
            case "medication":
                return "Inventory Hub";
            case "sales":
                return "Sales Hub";
            case "staff":
                return "Staff Hub";
            default:
                return "Vanella Pharmacy";
        }
    });
</script>

<template>
    <div class="mt-14 md:mt-0 md:flex h-screen w-screen">
        <header class="min-w-[220px] max-w-[220px]">
            <div
                class="fixed top-0 md:hidden p-3 text-sm flex items-center justify-between bg-white shadow-md z-40 w-full"
            >
                <button @click="hamburger = !hamburger">
                    <i class="pi pi-align-left"></i>
                </button>
                <h1 class="text-2xl font-styleScript text-orange-600">
                    {{ tabLabel }}
                </h1>
                <RouterLink to="/login" class="text-gray-700">
                    <i class="pi pi-sign-out"></i>
                </RouterLink>
            </div>
            <!-- Sidebar for tablet view -->
            <div class="">
                <aside
                    :class="[
                        'fixed md:block top-0 z-50 md:min-w-[220px] shadow w-full md:max-w-[220px] bg-white h-screen text-gray-800 transition-all duration-500 ease-in-out transform',
                        hamburger
                            ? 'translate-x-0 opacity-100 blur-none'
                            : '-translate-x-full opacity-20 blur-sm pointer-events-none',
                        'md:translate-x-0 md:opacity-100 md:blur-none md:pointer-events-auto md:block',
                    ]"
                >
                    <div
                        class="pt-2 flex items-center gap-4 justify-end md:block"
                    >
                        <h1
                            class="font-styleScript text-2xl text-center py-2 md:py-6 text-orange-600 md:text-3xl"
                        >
                            Dashboard
                        </h1>
                        <button
                            @click="hamburger = !hamburger"
                            class="pr-2 md:hidden"
                        >
                            <i class="pi pi-align-right"></i>
                        </button>
                    </div>

                    <!-- Navigation Buttons -->
                    <nav class="md:flex flex-col">
                        <button
                            @click="
                                activeTab = 'home';
                                hamburger = false;
                            "
                            class="a-dashboard-navs"
                            :class="{
                                'bg-orange-600 text-white hover:bg-orange-500':
                                    activeTab === 'home',
                            }"
                        >
                            <i class="pi pi-home"></i> Home
                        </button>
                        <button
                            @click="
                                activeTab = 'medication';
                                hamburger = false;
                            "
                            class="a-dashboard-navs"
                            :class="{
                                'bg-orange-600 text-white hover:bg-orange-500':
                                    activeTab === 'medication',
                            }"
                        >
                            <i class="pi pi-shield"></i> Medications
                        </button>
                        <button
                            @click="
                                activeTab = 'orders';
                                hamburger = false;
                            "
                            class="a-dashboard-navs"
                            :class="{
                                'bg-orange-600 text-white hover:bg-orange-500':
                                    activeTab === 'orders',
                            }"
                        >
                            <i class="pi pi-cart-arrow-down"></i> Orders
                        </button>
                        <button
                            @click="
                                activeTab = 'cart';
                                hamburger = false;
                            "
                            class="a-dashboard-navs"
                            :class="{
                                'bg-orange-600 text-white hover:bg-orange-500':
                                    activeTab === 'cart',
                            }"
                        >
                            <i class="pi pi-cart-plus"></i> Cart
                        </button>
                        <button class="a-dashboard-navs">
                            <i class="pi pi-info-circle"></i> Notifications
                        </button>
                        <!-- Logout Button -->
                        <RouterLink to="/login" class="block">
                            <button
                                class="mt-16 md:mt-20 py-2 w-full pl-3 rounded font-medium text-sm flex items-center gap-4 text-gray-800 md:pl-5 hover:bg-gray-100 focus:bg-orange-600 focus:text-white"
                            >
                                <i class="pi pi-sign-out"></i> Logout
                            </button>
                        </RouterLink>
                    </nav>
                </aside>
            </div>
        </header>
        <main class="w-full h-screen bg-gray-100 overflow-auto">
            <div class="mx-auto">
                <HomeHero v-if="activeTab === 'home'" />
                <MedicationHero v-if="activeTab === 'medication'" />
            </div>
        </main>
    </div>
</template>
