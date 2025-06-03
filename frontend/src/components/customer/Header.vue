<script setup>
    import { ref, computed } from "vue";
    import { useRoute, useRouter } from "vue-router";
    import { useAuthStore } from "@/stores/auth";
    import { useMedStore } from "@/stores/medStore";

    const route = useRoute();
    const router = useRouter();

    const auth = useAuthStore();
    const medStore = useMedStore();

    const isAuthenticated = computed(() => auth.isAuthenticated);
    const showMobileNav = ref(false);
    const searchTerm = ref("");
    const isSearching = ref(false);
    const searchResults = computed(() => medStore.searchResults);

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
            class="w-full flex items-center justify-between p-4 gap-6 lg:px-10 lg:py-4 bg-white shadow-md fixed top-0 z-50"
        >
            <router-link
                to="/"
                class="text-orange-600 flex items-center gap-2 font-semibold"
            >
                <i class="pi pi-slack text-2xl"></i>VPharm
            </router-link>

            <!-- Desktop Search -->
            <div
                class="hidden md:flex items-center w-full md:max-w-sm lg:max-w-md relative"
            >
                <input
                    v-model="searchTerm"
                    @input="performSearch"
                    type="search"
                    placeholder="Search..."
                    class="w-full px-4 py-1 text-gray-700 border focus:outline-none focus:border-orange-700 bg-white shadow rounded-l-full"
                />
                <button
                    class="flex items-center justify-center border border-orange-600 bg-orange-600 text-white px-4 py-1 rounded-r-full hover:bg-orange-700 transition"
                >
                    <i class="pi pi-search text-base"></i>
                </button>

                <!-- Search Result Dropdown -->
                <div
                    v-if="searchTerm && !isSearching"
                    class="absolute top-full mt-1 left-0 w-full bg-white shadow-lg rounded-md z-50 max-h-60 overflow-auto"
                >
                    <ul>
                        <li
                            v-for="result in searchResults"
                            :key="result.id"
                            @click="goToProductDetails(result.id)"
                            class="px-4 py-2 hover:bg-orange-100 cursor-pointer text-sm text-gray-800"
                        >
                            {{ result.name }}
                        </li>
                        <li
                            v-if="searchResults.length === 0"
                            class="px-4 py-2 text-sm text-gray-500"
                        >
                            No match found
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Desktop Nav -->
            <nav class="hidden lg:flex items-center gap-6">
                <router-link
                    v-if="isAuthenticated"
                    to="/"
                    :class="[
                        'text-gray-700 border-b-2 transition-all duration-500',
                        route.path === '/'
                            ? 'border-orange-600 text-orange-600'
                            : 'border-white hover:border-orange-600 hover:text-orange-600',
                    ]"
                >
                    Home
                </router-link>

                <router-link
                    v-if="isAuthenticated"
                    to="/carts"
                    class="text-gray-700 transition-all duration-500 hover:text-orange-600"
                >
                    Carts
                </router-link>

                <router-link
                    v-if="isAuthenticated"
                    to="/orders"
                    class="text-gray-700 transition-all duration-500 hover:text-orange-600"
                >
                    Orders
                </router-link>

                <button
                    v-if="isAuthenticated"
                    @click="handleLogout"
                    class="text-gray-700 transition-all duration-500 hover:text-orange-600"
                >
                    Logout
                </button>

                <router-link
                    v-if="!isAuthenticated"
                    to="/login"
                    class="text-gray-700 transition-all duration-500 hover:text-orange-600"
                >
                    Login
                </router-link>

                <router-link
                    v-if="!isAuthenticated"
                    to="/register"
                    class="text-gray-700 transition-all duration-500 hover:text-orange-600"
                >
                    Register
                </router-link>
            </nav>

            <!-- Mobile Nav Toggle -->
            <button
                @click="toggleMobileNav"
                class="lg:hidden text-2xl text-orange-600 focus:outline-none"
                aria-label="Toggle mobile navigation"
            >
                <i :class="showMobileNav ? 'pi pi-times' : 'pi pi-bars'"></i>
            </button>
        </div>

        <!-- Mobile Search Bar (shows only when mobile nav is closed) -->
        <div
            v-if="!showMobileNav"
            class="md:hidden fixed top-[64px] inset-x-0 px-4 py-2 z-40"
        >
            <div class="flex items-center w-full relative">
                <input
                    v-model="searchTerm"
                    @input="performSearch"
                    type="search"
                    placeholder="Search..."
                    class="w-full px-4 py-2 text-gray-700 border border-gray-500 focus:outline-none focus:border-orange-600 bg-white rounded-l-full"
                />
                <button
                    class="px-4 py-2 border border-orange-600 bg-orange-600 text-white rounded-r-full hover:bg-orange-700"
                    aria-label="Mobile search button"
                >
                    <i class="pi pi-search text-base"></i>
                </button>
            </div>

            <!-- Mobile Search Result Dropdown -->
            <div
                v-if="searchTerm && !isSearching"
                class="bg-white shadow rounded-md z-50 max-h-60 overflow-auto"
            >
                <ul>
                    <li
                        v-for="result in searchResults"
                        :key="result.id"
                        @click="goToProductDetails(result.id)"
                        class="px-4 py-2 hover:bg-orange-100 cursor-pointer text-sm text-gray-800"
                    >
                        {{ result.name }}
                    </li>
                    <li
                        v-if="searchResults.length === 0"
                        class="px-4 py-2 text-sm text-gray-500"
                    >
                        No match found
                    </li>
                </ul>
            </div>
        </div>

        <!-- Mobile Nav (shows only when mobile nav is open) -->
        <transition name="fade">
            <nav
                v-if="showMobileNav"
                class="lg:hidden fixed top-[64px] inset-x-0 bg-white z-50 shadow-lg p-4 space-y-4"
            >
                <router-link
                    v-if="isAuthenticated"
                    to="/"
                    :class="[
                        'block text-gray-700 border-r-4 pr-2',
                        route.path === '/'
                            ? 'border-orange-600 text-orange-600'
                            : 'border-white hover:border-orange-600 hover:text-orange-600',
                    ]"
                    @click="toggleMobileNav"
                >
                    Home
                </router-link>

                <router-link
                    v-if="isAuthenticated"
                    to="/carts"
                    class="block text-gray-700 border-r-4 pr-2"
                    @click="toggleMobileNav"
                >
                    Carts
                </router-link>

                <router-link
                    v-if="isAuthenticated"
                    to="/orders"
                    :class="[
                        'block text-gray-700 border-r-4 pr-2',
                        route.path === '/orders'
                            ? 'border-orange-600 text-orange-600'
                            : 'border-white hover:border-orange-600 hover:text-orange-600',
                    ]"
                    @click="toggleMobileNav"
                >
                    Orders
                </router-link>

                <button
                    v-if="isAuthenticated"
                    @click="
                        () => {
                            handleLogout();
                            toggleMobileNav();
                        }
                    "
                    class="block w-full text-left text-gray-700 hover:text-orange-600"
                >
                    Logout
                </button>

                <router-link
                    v-if="!isAuthenticated"
                    to="/login"
                    class="block text-gray-700"
                    @click="toggleMobileNav"
                >
                    Login
                </router-link>

                <router-link
                    v-if="!isAuthenticated"
                    to="/register"
                    class="block text-gray-700"
                    @click="toggleMobileNav"
                >
                    Register
                </router-link>
            </nav>
        </transition>
    </header>
</template>
