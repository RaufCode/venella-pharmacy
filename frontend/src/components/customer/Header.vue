<script setup>
    import { ref, computed, onMounted } from "vue";
    import { useRoute, useRouter } from "vue-router";
    import { useAuthStore } from "@/stores/auth";
    import { useMedStore } from "@/stores/medStore";
    import { useNotificationStore } from "@/stores/notification"; // ✅ Import

    const route = useRoute();
    const router = useRouter();

    const auth = useAuthStore();
    const medStore = useMedStore();
    const notificationStore = useNotificationStore(); // ✅ Init notification store

    const isAuthenticated = computed(() => auth.isAuthenticated);
    const showMobileNav = ref(false);
    const searchTerm = ref("");
    const isSearching = ref(false);
    const searchResults = computed(() => medStore.searchResults);

    // ✅ Fetch notifications when authenticated and mounted
    onMounted(() => {
        if (isAuthenticated.value) {
            notificationStore.fetchNotifications();
            notificationStore.startPolling();
        }
    });

    // ✅ Computed unread count
    const unreadCount = computed(
        () => notificationStore.notifications.filter((n) => !n.read).length
    );

    function toggleMobileNav() {
        showMobileNav.value = !showMobileNav.value;
    }

    function handleLogout() {
        auth.logout();
    }

    async function performSearch() {
        if (!searchTerm.value.trim()) {
            medStore.searchResults = [];
            return;
        }

        isSearching.value = true;
        await medStore.searchProducts(searchTerm.value);
        isSearching.value = false;
    }

    function goToProductDetails(productId) {
        medStore.searchResults = [];
        searchTerm.value = "";
        router.push(`/product/${productId}`);
    }
</script>

<template>
    <header class="relative">
        <div
            class="w-full flex items-center justify-between p-4 gap-6 lg:px-10 lg:py-4 bg-white shadow-lg border-b border-gray-100 fixed top-0 z-50"
        >
            <router-link
                to="/"
                class="text-orange-600 flex items-center gap-2 font-bold text-lg hover:text-orange-700 transition-colors"
            >
                <div class="w-8 h-8 bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">
                    V
                </div>
                VPharm
            </router-link>

            <!-- Desktop Search -->
            <div
                class="hidden md:flex items-center w-full md:max-w-sm lg:max-w-md relative"
            >
                <div class="relative w-full">
                    <input
                        v-model="searchTerm"
                        @input="performSearch"
                        type="search"
                        placeholder="Search for medications..."
                        class="w-full pl-10 pr-4 py-2.5 text-gray-700 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-white rounded-l-lg placeholder-gray-400"
                    />
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <i class="pi pi-search text-gray-400"></i>
                    </div>
                </div>
                <button
                    class="flex items-center justify-center bg-gradient-to-r from-orange-500 to-orange-600 text-white px-4 py-2.5 rounded-r-lg hover:from-orange-600 hover:to-orange-700 transition-all duration-200 shadow-md"
                >
                    <i class="pi pi-search text-base"></i>
                </button>

                <!-- Search Result Dropdown -->
                <div
                    v-if="searchTerm && !isSearching"
                    class="absolute top-full mt-2 left-0 w-full bg-white shadow-xl rounded-lg border border-gray-200 z-50 max-h-60 overflow-auto"
                >
                    <ul class="py-2">
                        <li
                            v-for="result in searchResults"
                            :key="result.id"
                            @click="goToProductDetails(result.id)"
                            class="px-4 py-3 hover:bg-orange-50 cursor-pointer text-sm text-gray-800 border-b border-gray-100 last:border-b-0 transition-colors"
                        >
                            <div class="flex items-center gap-3">
                                <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                                <span class="font-medium">{{ result.name }}</span>
                            </div>
                        </li>
                        <li
                            v-if="searchResults.length === 0"
                            class="px-4 py-3 text-sm text-gray-500 text-center"
                        >
                            <div class="flex items-center justify-center gap-2">
                                <i class="pi pi-search text-gray-400"></i>
                                <span>No medications found</span>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Desktop Nav -->
            <nav class="hidden lg:flex items-center gap-6">
                <router-link
                    v-if="isAuthenticated"
                    to="/notification"
                    class="relative text-gray-600 hover:text-orange-600 transition-colors p-2 rounded-lg hover:bg-orange-50"
                >
                    <i class="pi pi-bell text-xl"></i>
                    <span
                        v-if="unreadCount > 0"
                        class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center font-medium"
                    >
                        {{ unreadCount > 9 ? '9+' : unreadCount }}
                    </span>
                </router-link>

                <router-link
                    v-if="isAuthenticated"
                    to="/"
                    :class="[
                        'px-3 py-2 rounded-lg font-medium transition-all duration-200',
                        route.path === '/'
                            ? 'bg-orange-100 text-orange-600 border border-orange-200'
                            : 'text-gray-600 hover:text-orange-600 hover:bg-orange-50',
                    ]"
                >
                    Home
                </router-link>

                <router-link
                    v-if="isAuthenticated"
                    to="/carts"
                    class="px-3 py-2 rounded-lg font-medium text-gray-600 hover:text-orange-600 hover:bg-orange-50 transition-all duration-200"
                >
                    Cart
                </router-link>

                <router-link
                    v-if="isAuthenticated"
                    to="/orders"
                    class="px-3 py-2 rounded-lg font-medium text-gray-600 hover:text-orange-600 hover:bg-orange-50 transition-all duration-200"
                >
                    Orders
                </router-link>

                <button
                    v-if="isAuthenticated"
                    @click="handleLogout"
                    class="px-4 py-2 bg-gray-100 text-gray-600 hover:bg-red-50 hover:text-red-600 rounded-lg font-medium transition-all duration-200 border border-gray-200"
                >
                    Logout
                </button>

                <div v-if="!isAuthenticated" class="flex items-center gap-3">
                    <router-link
                        to="/login"
                        class="px-4 py-2 text-gray-600 hover:text-orange-600 font-medium transition-colors"
                    >
                        Login
                    </router-link>

                    <router-link
                        to="/register"
                        class="px-4 py-2 bg-gradient-to-r from-orange-500 to-orange-600 text-white hover:from-orange-600 hover:to-orange-700 rounded-lg font-medium transition-all duration-200 shadow-md"
                    >
                        Register
                    </router-link>
                </div>
            </nav>

            <!-- Mobile Right: Notification + Hamburger -->
            <div class="flex items-center gap-4 lg:hidden">
                <router-link
                    v-if="isAuthenticated"
                    to="/notification"
                    class="relative p-2 text-gray-600 hover:text-orange-600 transition-colors"
                >
                    <i class="pi pi-bell text-xl"></i>
                    <span
                        v-if="unreadCount > 0"
                        class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center font-medium"
                    >
                        {{ unreadCount > 9 ? '9+' : unreadCount }}
                    </span>
                </router-link>

                <button
                    @click="toggleMobileNav"
                    class="p-2 text-orange-600 hover:bg-orange-50 rounded-lg transition-colors focus:outline-none"
                    aria-label="Toggle mobile navigation"
                >
                    <i
                        :class="showMobileNav ? 'pi pi-times' : 'pi pi-bars'"
                        class="text-xl"
                    ></i>
                </button>
            </div>
        </div>

        <!-- Mobile Search Bar -->
        <div
            v-if="!showMobileNav"
            class="md:hidden fixed top-[80px] inset-x-0 px-4 py-3 z-40 bg-white border-b border-gray-100"
        >
            <div class="flex items-center w-full relative">
                <div class="relative w-full">
                    <input
                        v-model="searchTerm"
                        @input="performSearch"
                        type="search"
                        placeholder="Search for medications..."
                        class="w-full pl-10 pr-4 py-2.5 text-gray-700 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-white rounded-l-lg placeholder-gray-400"
                    />
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <i class="pi pi-search text-gray-400"></i>
                    </div>
                </div>
                <button
                    class="px-4 py-2.5 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-r-lg hover:from-orange-600 hover:to-orange-700 transition-all duration-200 shadow-md"
                    aria-label="Mobile search button"
                >
                    <i class="pi pi-search text-base"></i>
                </button>
            </div>

            <!-- Mobile Search Result Dropdown -->
            <div
                v-if="searchTerm && !isSearching"
                class="mt-2 bg-white shadow-xl rounded-lg border border-gray-200 max-h-60 overflow-auto"
            >
                <ul class="py-2">
                    <li
                        v-for="result in searchResults"
                        :key="result.id"
                        @click="goToProductDetails(result.id)"
                        class="px-4 py-3 hover:bg-orange-50 cursor-pointer text-sm text-gray-800 border-b border-gray-100 last:border-b-0 transition-colors"
                    >
                        <div class="flex items-center gap-3">
                            <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                            <span class="font-medium">{{ result.name }}</span>
                        </div>
                    </li>
                    <li
                        v-if="searchResults.length === 0"
                        class="px-4 py-3 text-sm text-gray-500 text-center"
                    >
                        <div class="flex items-center justify-center gap-2">
                            <i class="pi pi-search text-gray-400"></i>
                            <span>No medications found</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>

        <!-- Mobile Nav -->
        <transition name="fade">
            <nav
                v-if="showMobileNav"
                class="lg:hidden fixed top-[80px] inset-x-0 bg-white z-50 shadow-xl border-t border-gray-100"
            >
                <div class="px-4 py-6 space-y-4">
                    <router-link
                        v-if="isAuthenticated"
                        to="/"
                        :class="[
                            'flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-all duration-200',
                            route.path === '/'
                                ? 'bg-orange-100 text-orange-600 border border-orange-200'
                                : 'text-gray-600 hover:text-orange-600 hover:bg-orange-50',
                        ]"
                        @click="toggleMobileNav"
                    >
                        <i class="pi pi-home text-lg"></i>
                        <span>Home</span>
                    </router-link>

                    <router-link
                        v-if="isAuthenticated"
                        to="/carts"
                        class="flex items-center gap-3 px-4 py-3 rounded-lg font-medium text-gray-600 hover:text-orange-600 hover:bg-orange-50 transition-all duration-200"
                        @click="toggleMobileNav"
                    >
                        <i class="pi pi-shopping-cart text-lg"></i>
                        <span>Cart</span>
                    </router-link>

                    <router-link
                        v-if="isAuthenticated"
                        to="/orders"
                        class="flex items-center gap-3 px-4 py-3 rounded-lg font-medium text-gray-600 hover:text-orange-600 hover:bg-orange-50 transition-all duration-200"
                        @click="toggleMobileNav"
                    >
                        <i class="pi pi-package text-lg"></i>
                        <span>Orders</span>
                    </router-link>

                    <button
                        v-if="isAuthenticated"
                        @click="
                            () => {
                                handleLogout();
                                toggleMobileNav();
                            }
                        "
                        class="flex items-center gap-3 px-4 py-3 rounded-lg font-medium text-gray-600 hover:text-red-600 hover:bg-red-50 transition-all duration-200 w-full text-left"
                    >
                        <i class="pi pi-sign-out text-lg"></i>
                        <span>Logout</span>
                    </button>

                    <div v-if="!isAuthenticated" class="space-y-3 pt-4 border-t border-gray-200">
                        <router-link
                            to="/login"
                            class="flex items-center gap-3 px-4 py-3 rounded-lg font-medium text-gray-600 hover:text-orange-600 hover:bg-orange-50 transition-all duration-200"
                            @click="toggleMobileNav"
                        >
                            <i class="pi pi-sign-in text-lg"></i>
                            <span>Login</span>
                        </router-link>

                        <router-link
                            to="/register"
                            class="flex items-center gap-3 px-4 py-3 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg font-medium transition-all duration-200 shadow-md"
                            @click="toggleMobileNav"
                        >
                            <i class="pi pi-user-plus text-lg"></i>
                            <span>Register</span>
                        </router-link>
                    </div>
                </div>
            </nav>
        </transition>
    </header>
</template>
