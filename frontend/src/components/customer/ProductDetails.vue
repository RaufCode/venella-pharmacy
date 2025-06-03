<script setup>
    import { ref, onMounted, computed } from "vue";
    import { useRoute, useRouter } from "vue-router";
    import axios from "axios";
    import { useCartStore } from "@/stores/cartStore";
    import { useAuthStore } from "@/stores/auth"; // <-- import auth store
    import { storeToRefs } from "pinia";

    const route = useRoute();
    const router = useRouter();

    const product = ref(null);
    const loading = ref(true);

    // Cart store setup
    const cartStore = useCartStore();
    const { carts, cartLoading } = storeToRefs(cartStore);

    // Auth store setup
    const auth = useAuthStore();

    // Load single product
    onMounted(async () => {
        try {
            const res = await axios.get(
                `/api/products/${route.params.id}/retrieve/`
            );
            product.value = res.data;
        } catch (err) {
            console.error("Failed to fetch product:", err);
        } finally {
            loading.value = false;
        }

        // Removed: await cartStore.fetchCartItems();
    });

    // Helpers
    const isInCart = computed(() =>
        product.value
            ? carts.value.some((item) => item.product?.id === product.value.id)
            : false
    );

    const getProductQuantity = computed(() => {
        if (!product.value) return 0;
        const item = carts.value.find(
            (item) => item.product?.id === product.value.id
        );
        return item ? item.quantity : 0;
    });

    // Handler: add or increment, with auth check
    const handleAddOrIncrement = async () => {
        if (!product.value) return;

        if (!auth.isAuthenticated) {
            // Redirect to login if not logged in
            router.push({
                path: "/login",
                query: { redirect: route.fullPath },
            });
            return;
        }

        if (!isInCart.value) {
            await cartStore.addToCart(product.value.id);
        } else {
            await cartStore.incrementQuantity(product.value.id);
        }
    };

    const handleDecrement = async () => {
        if (!product.value) return;
        await cartStore.decrementQuantity(product.value.id);
    };
</script>

<template>
    <div
        class="min-h-screen bg-gray-50 p-4 sm:p-6 lg:p-12 flex items-center justify-center"
    >
        <div class="max-w-6xl w-full">
            <!-- Go Back Button -->
            <button
                @click="$router.back()"
                class="text-orange-600 text-sm font-medium flex items-center gap-1 mb-6"
            >
                <i class="pi pi-arrow-left mr-2"></i>
                Go Back
            </button>

            <!-- Loading Spinner -->
            <div v-if="loading" class="flex justify-center items-center py-10">
                <i class="pi pi-spinner pi-spin text-3xl text-orange-600"></i>
                <span class="ml-3 text-gray-600">Loading product...</span>
            </div>

            <!-- Product Details -->
            <div v-else class="flex flex-col lg:flex-row gap-8 p-5">
                <!-- Left: Image -->
                <div class="flex-1">
                    <img
                        v-if="product?.images?.[0]?.image"
                        :src="`https://techrems.pythonanywhere.com${product.images[0].image}`"
                        :alt="product.name"
                        class="w-full max-h-[400px] object-contain rounded-xl"
                        @error="$event.target.src = '/placeholder-image.jpg'"
                    />
                </div>

                <!-- Right: Info & Actions -->
                <div class="w-full lg:w-[450px] space-y-4 text-sm sm:text-base">
                    <!-- Tags -->
                    <div class="flex items-center gap-2">
                        <span
                            class="bg-orange-100 text-orange-600 px-3 py-1 rounded-full text-xs font-medium"
                            >Official Store</span
                        >
                        <span
                            class="bg-pink-100 text-pink-600 px-3 py-1 rounded-full text-xs font-medium"
                            >Anniversary Deal</span
                        >
                    </div>

                    <!-- Name & Description -->
                    <h1 class="font-semibold text-gray-800 text-xl">
                        {{ product.name }}
                    </h1>
                    <p class="text-gray-800 text-justify">
                        {{ product.description }}
                    </p>

                    <!-- Add to Cart -->
                    <div class="flex gap-4 items-center mt-4">
                        <button
                            v-if="!isInCart"
                            @click="handleAddOrIncrement"
                            class="bg-orange-600 hover:bg-orange-700 text-white py-2 px-4 sm:py-3 sm:px-6 rounded w-full text-sm sm:text-base font-medium"
                            :disabled="cartLoading[product.id]"
                        >
                            <span v-if="cartLoading[product.id]">
                                <i class="pi pi-spinner pi-spin text-white"></i>
                            </span>
                            <span v-else>
                                <i class="pi pi-cart-plus mr-2"></i> Add to Cart
                            </span>
                        </button>

                        <div v-else class="flex items-center gap-4">
                            <button
                                @click="handleDecrement"
                                class="w-8 h-8 rounded-full bg-orange-700 text-white text-xl flex items-center justify-center"
                                title="Decrease quantity"
                            >
                                &minus;
                            </button>
                            <span class="font-semibold">{{
                                getProductQuantity
                            }}</span>
                            <button
                                @click="handleAddOrIncrement"
                                class="w-8 h-8 rounded-full bg-orange-700 text-white text-xl flex items-center justify-center"
                                title="Increase quantity"
                            >
                                +
                            </button>
                        </div>
                    </div>

                    <!-- Pricing -->
                    <div>
                        <p class="text-orange-600 font-bold text-lg">
                            GH₵ {{ product.price }}
                        </p>
                        <p
                            v-if="product.discount"
                            class="text-green-600 text-sm font-medium"
                        >
                            {{ product.discount }}% OFF
                        </p>
                        <p class="text-red-600 text-sm">Few units left</p>
                    </div>

                    <!-- Delivery Info -->
                    <div class="bg-gray-100 p-3 rounded-md text-sm">
                        <p class="text-green-700 font-semibold">
                            Delivery is not free
                        </p>
                    </div>

                    <!-- Ratings -->
                    <div
                        class="flex items-center text-yellow-500 gap-1 text-sm"
                    >
                        <i class="pi pi-star-fill" v-for="n in 4" :key="n"></i>
                        <i class="pi pi-star"></i>
                        <span class="text-gray-600 ml-2"
                            >({{ product.ratings }} verified ratings)</span
                        >
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
