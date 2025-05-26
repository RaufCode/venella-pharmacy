<script setup>
    import { ref, computed, onMounted } from "vue";
    import { useAuthStore } from "@/stores/auth";

    const auth = useAuthStore();
    const showMobileNav = ref(false);

    // Initialize auth on mount
    onMounted(() => {
        auth.initializeAuth();
    });

    const isReady = computed(() => auth.ready); // wait until auth state is loaded
    const isAuthenticated = computed(() => auth.isAuthenticated);

    function toggleMobileNav() {
        showMobileNav.value = !showMobileNav.value;
    }

    function handleLogout() {
        auth.logout();
    }

    const products = ref([
        {
            id: 1,
            name: "Paracetamol 500mg",
            description: "Fast relief from headaches and fever.",
            price: 20,
            image: "/drug1.jpg",
            rating: 5,
        },
        {
            id: 2,
            name: "Amoxicillin 250mg",
            description: "Broad-spectrum antibiotic for infections.",
            price: 35,
            image: "/drug2.jpg",
            rating: 4,
        },
    ]);
</script>

<template>
    <div v-if="isReady">
        <header class="relative">
            <!-- Top Navbar -->
            <div
                class="w-full flex items-center justify-between p-4 gap-6 lg:px-10 lg:py-4 bg-white shadow-md fixed top-0 z-50"
            >
                <!-- Logo -->
                <router-link
                    to="/"
                    class="text-orange-600 flex items-center gap-2 font-semibold"
                >
                    <i class="pi pi-slack text-2xl"></i>VPharm
                </router-link>

                <!-- Search Bar (md+) -->
                <div
                    class="hidden md:flex items-center w-full md:max-w-sm lg:max-w-md bg-white shadow rounded-full"
                >
                    <input
                        type="search"
                        placeholder="Search..."
                        class="w-full px-4 py-1 text-gray-700 border focus:outline-none focus:border-orange-700 bg-transparent rounded-l-full"
                    />
                    <button
                        class="flex items-center justify-center border border-orange-600 bg-orange-600 text-white px-4 py-1 rounded-r-full hover:bg-orange-700 transition"
                    >
                        <i class="pi pi-search text-base"></i>
                    </button>
                </div>

                <!-- Desktop Navigation (lg+) -->
                <nav class="hidden lg:flex items-center gap-6">
                    <router-link
                        v-if="isAuthenticated"
                        to="/"
                        class="text-gray-700 hover:text-orange-600"
                        >Home</router-link
                    >
                    <router-link
                        v-if="isAuthenticated"
                        to="/carts"
                        class="text-gray-700 hover:text-orange-600"
                        >Carts</router-link
                    >
                    <router-link
                        v-if="isAuthenticated"
                        to="/orders"
                        class="text-gray-700 hover:text-orange-600"
                        >Orders</router-link
                    >
                    <button
                        v-if="isAuthenticated"
                        @click="handleLogout"
                        class="text-gray-700 hover:text-orange-600"
                    >
                        Logout
                    </button>
                    <router-link
                        v-if="!isAuthenticated"
                        to="/login"
                        class="text-gray-700 hover:text-orange-600"
                        >Login</router-link
                    >
                    <router-link
                        v-if="!isAuthenticated"
                        to="/register"
                        class="text-gray-700 hover:text-orange-600"
                        >Register</router-link
                    >
                </nav>

                <!-- Hamburger Icon (lg−) -->
                <button
                    @click="toggleMobileNav"
                    class="lg:hidden text-2xl text-orange-600 focus:outline-none"
                    aria-label="Toggle mobile navigation"
                >
                    <i
                        :class="showMobileNav ? 'pi pi-times' : 'pi pi-bars'"
                    ></i>
                </button>
            </div>

            <!-- Mobile Navigation -->
            <transition name="fade">
                <nav
                    v-if="showMobileNav"
                    class="lg:hidden fixed top-[65px] inset-x-0 bg-white z-40 shadow-lg p-4 space-y-4"
                >
                    <router-link
                        v-if="isAuthenticated"
                        to="/"
                        class="block text-gray-700 hover:text-orange-600"
                        @click="toggleMobileNav"
                        >Home</router-link
                    >
                    <router-link
                        v-if="isAuthenticated"
                        to="/carts"
                        class="block text-gray-700 hover:text-orange-600"
                        @click="toggleMobileNav"
                        >Carts</router-link
                    >
                    <router-link
                        v-if="isAuthenticated"
                        to="/orders"
                        class="block text-gray-700 hover:text-orange-600"
                        @click="toggleMobileNav"
                        >Orders</router-link
                    >
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
                        class="block text-gray-700 hover:text-orange-600"
                        @click="toggleMobileNav"
                        >Login</router-link
                    >
                    <router-link
                        v-if="!isAuthenticated"
                        to="/register"
                        class="block text-gray-700 hover:text-orange-600"
                        @click="toggleMobileNav"
                        >Register</router-link
                    >
                </nav>
            </transition>
        </header>

        <main class="min-h-screen">
            <!-- Top Banner -->
            <section class="bg-gray-50">
                <div class="container mx-auto px-4 lg:px-10">
                    <h1
                        class="text-sm md:text-2xl text-left pt-20 md:pt-24 md:pb-8 font-medium"
                    >
                        WELCOME TO VENELLA PHARMACY
                    </h1>

                    <!-- Mobile Search -->
                    <div class="flex items-center w-full pt-2 pb-5 md:hidden">
                        <input
                            type="search"
                            placeholder="Search..."
                            class="w-full px-4 py-1 text-black border border-black focus:outline-none focus:border-orange-700 bg-transparent rounded-l-full"
                        />
                        <button
                            class="flex items-center justify-center border border-orange-600 bg-orange-600 text-white px-4 py-1 rounded-r-full hover:bg-orange-700 transition"
                        >
                            <i class="pi pi-search text-base"></i>
                        </button>
                    </div>
                </div>
            </section>

            <!-- Product Section -->
            <section class="container mx-auto px-4 lg:px-10">
                <h1 class="py-3 text-xl md:py-7 md:text-2xl font-medium">
                    Products Available
                </h1>
                <div
                    class="grid place-items-center grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4 w-full mb-5 cursor-pointer"
                >
                    <article
                        v-for="product in products"
                        :key="product.id"
                        class="bg-white p-2 rounded-2xl border shadow overflow-hidden w-full max-w-xs hover:shadow-lg transition-shadow duration-300"
                    >
                        <div class="h-40 bg-gray-100 rounded-t-xl">
                            <img
                                :src="product.image"
                                :alt="product.name"
                                class="w-full h-full object-cover rounded-t-xl"
                            />
                        </div>
                        <div class="p-4 space-y-2">
                            <div class="flex gap-1 text-yellow-500 text-sm">
                                <i
                                    v-for="n in product.rating"
                                    :key="n"
                                    class="pi pi-heart-fill"
                                ></i>
                            </div>
                            <p
                                class="text-gray-700 text-sm font-semibold truncate"
                            >
                                {{ product.name }}
                            </p>
                            <p class="text-gray-600 text-sm truncate">
                                {{ product.description }}
                            </p>
                            <div class="flex justify-between items-center mt-2">
                                <p class="text-orange-600 font-bold">
                                    ₵{{ product.price }}
                                </p>
                                <button
                                    class="bg-orange-600 hover:bg-orange-700 text-white px-4 py-3 rounded-full"
                                >
                                    <i class="pi pi-cart-plus"></i>
                                </button>
                            </div>
                        </div>
                    </article>
                </div>
            </section>
        </main>

        <footer>
            <div class="py-4 text-center text-gray-400 text-sm bg-gray-800">
                <p>&copy; Vanelle Pharmacy - All Rights Reserved</p>
            </div>
            <div class="bg-gray-800 px-4 md:px-6 lg:px-10 pt-2">
                <div
                    class="max-w-[1440px] border-t border-gray-400 pt-5 md:mx-auto md:w-[300px] lg:w-auto"
                >
                    <p class="text-white text-lg font-semibold flex gap-3 pb-4">
                        <i class="pi pi-slack text-blue-600 text-2xl"></i
                        >venella pharmacy
                    </p>
                </div>
            </div>
        </footer>
    </div>
</template>

<style scoped>
    .fade-enter-active,
    .fade-leave-active {
        transition: all 0.3s ease;
    }
    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
        transform: translateY(-10px);
    }
</style>
