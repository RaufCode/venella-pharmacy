<script setup>
    import { ref, computed } from "vue";
    import OverView from "./OverView.vue";
    import MedicationHero from "./MedicationHero.vue";
    import SalesHero from "../salesperson-dashboard/SalesHero.vue";
    import StaffHero from "./StaffHero.vue";
    import { RouterLink, useRouter } from "vue-router";
    import { useAuthStore } from "@/stores/auth";
    import Notifications from "./Notifications.vue";

    const auth = useAuthStore();
    const router = useRouter();

    const activeTab = ref("overview");
    const hamburger = ref(false);
    const notificationCount = ref(3); // Replace with your actual dynamic count

    const tabLabel = computed(() => {
        switch (activeTab.value) {
            case "overview":
                return "Overview";
            case "medication":
                return "Inventory Hub";
            case "sales":
                return "Sales Hub";
            case "staff":
                return "Staff Hub";
            case "notification":
                return "Notifications Hub";
            default:
                return "Vanella Pharmacy";
        }
    });

    function handleLogout() {
        auth.logout();
        router.push("/login");
    }
</script>

<template>
    <div class="pt-9 md:pt-0 md:flex h-screen w-screen">
        <!-- Top Bar (Mobile) -->
        <header class="">
            <div
                class="fixed top-0 md:hidden p-3 text-sm flex items-center justify-between bg-white shadow-md z-40 w-full"
            >
                <button
                    @click="hamburger = !hamburger"
                    aria-label="Open sidebar"
                    class="focus:outline-none"
                >
                    <i class="pi pi-align-left"></i>
                </button>
                <h1 class="text-2xl font-styleScript text-orange-600">
                    {{ tabLabel }}
                </h1>
                <button
                    @click="handleLogout"
                    aria-label="Logout"
                    class="text-gray-700 focus:outline-none"
                >
                    <i class="pi pi-sign-out"></i>
                </button>
            </div>

            <!-- Overlay (Mobile) -->
            <div
                v-if="hamburger"
                @click="hamburger = false"
                class="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
                aria-hidden="true"
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
                tabindex="-1"
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
                        class="pr-2 md:hidden focus:outline-none"
                        aria-label="Close sidebar"
                    >
                        <i class="pi pi-times"></i>
                    </button>
                </div>

                <!-- Navigation Buttons -->
                <nav
                    class="md:flex flex-col gap-6"
                    aria-label="Main navigation"
                >
                    <button
                        v-for="tab in [
                            {
                                key: 'overview',
                                icon: 'pi-home',
                                label: 'Overview',
                            },
                            {
                                key: 'medication',
                                icon: 'pi-shield',
                                label: 'Medications',
                            },
                            { key: 'sales', icon: 'pi-book', label: 'Sales' },
                            { key: 'staff', icon: 'pi-users', label: 'Staff' },
                            {
                                key: 'notification',
                                icon: 'pi pi-bell',
                                label: 'Notification',
                            },
                        ]"
                        :key="tab.key"
                        @click="
                            activeTab = tab.key;
                            hamburger = false;
                        "
                        class="relative a-dashboard-navs"
                        :class="{
                            'bg-orange-600 text-white hover:bg-orange-500':
                                activeTab === tab.key,
                            'hover:bg-gray-100': activeTab !== tab.key,
                        }"
                        :aria-current="
                            activeTab === tab.key ? 'page' : undefined
                        "
                    >
                        <i :class="`pi ${tab.icon}`"></i>
                        {{ tab.label }}

                        <!-- Notification badge -->
                        <span
                            v-if="
                                tab.key === 'notification' &&
                                notificationCount > 0
                            "
                            class="absolute top-0 right-[108px] md:right-16 lg:right-24 bg-red-600 text-white text-xs px-1.5 py-0.5 rounded-full"
                        >
                            {{ notificationCount }}
                        </span>
                    </button>

                    <button
                        @click="handleLogout"
                        class="mt-16 md:mt-20 py-2 w-full pl-3 rounded font-medium text-sm flex items-center gap-4 text-gray-800 md:pl-5 hover:bg-gray-100 focus:bg-orange-600 focus:text-white"
                    >
                        <i class="pi pi-sign-out"></i> Logout
                    </button>
                </nav>
            </aside>
        </header>

        <!-- Main Content -->
        <main class="w-full h-screen overflow-auto">
            <div class="mx-auto">
                <OverView v-if="activeTab === 'overview'" />
                <MedicationHero v-if="activeTab === 'medication'" />
                <SalesHero v-if="activeTab === 'sales'" />
                <StaffHero v-if="activeTab === 'staff'" />
                <Notifications v-if="activeTab === 'notification'" />
            </div>
        </main>
    </div>
</template>

<style scoped>
    /* Add any custom styles here if needed */
</style>
