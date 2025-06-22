<script setup>
    import { ref, onMounted, computed } from "vue";
    import { useRoute, useRouter } from "vue-router";
    import axios from "axios";
    import { useCartStore } from "@/stores/cartStore";
    import { useAuthStore } from "@/stores/auth"; // <-- import auth store
    import { storeToRefs } from "pinia";
    import Spinner from "../ui/Spinner.vue";

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
    <div class="min-h-screen bg-gradient-to-br from-gray-50 to-white">
        <!-- Loading Spinner -->
        <div
            v-if="loading"
            class="flex items-center justify-center min-h-screen"
        >
            <div class="text-center">
                <Spinner />
                <p class="text-gray-600 mt-4">Loading product details...</p>
            </div>
        </div>

        <!-- Product Details -->
        <div v-else-if="product" class="pt-20 pb-10">
            <div class="container mx-auto px-4 lg:px-10">
                <!-- Back Button -->
                <button
                    @click="$router.back()"
                    class="mb-6 px-4 py-2 bg-white hover:bg-gray-50 text-gray-700 border border-gray-200 rounded-lg flex items-center gap-2 font-medium transition-all duration-200 shadow-sm hover:shadow-md"
                >
                    <i class="pi pi-arrow-left"></i>
                    <span>Back</span>
                </button>

                <!-- Product Content -->
                <div
                    class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100"
                >
                    <div
                        class="grid grid-cols-1 lg:grid-cols-2 gap-8 p-6 lg:p-8"
                    >
                        <!-- Left: Product Image -->
                        <div class="space-y-4">
                            <h2
                                class="text-lg font-semibold text-gray-800 lg:hidden"
                            >
                                Product Details
                            </h2>
                            <div
                                class="relative bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl overflow-hidden aspect-square lg:aspect-auto lg:h-96"
                            >
                                <img
                                    v-if="product?.images?.[0]?.image"
                                    :src="`https://techrems.pythonanywhere.com${product.images[0].image}`"
                                    :alt="product.name"
                                    class="w-full h-full object-contain p-6"
                                    @error="
                                        $event.target.src =
                                            '/placeholder-image.jpg'
                                    "
                                />
                                <div
                                    v-else
                                    class="flex items-center justify-center h-full"
                                >
                                    <div class="text-center">
                                        <i
                                            class="pi pi-image text-4xl text-gray-300 mb-2"
                                        ></i>
                                        <p class="text-gray-500 text-sm">
                                            No image available
                                        </p>
                                    </div>
                                </div>

                                <!-- Stock Badge -->
                                <div class="absolute top-4 left-4">
                                    <span
                                        :class="[
                                            'px-3 py-1 text-xs font-medium rounded-full',
                                            product.stock > 20
                                                ? 'bg-green-100 text-green-700'
                                                : product.stock > 0
                                                ? 'bg-yellow-100 text-yellow-700'
                                                : 'bg-red-100 text-red-700',
                                        ]"
                                    >
                                        {{
                                            product.stock > 20
                                                ? "In Stock"
                                                : product.stock > 0
                                                ? `${product.stock} left`
                                                : "Out of Stock"
                                        }}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- Right: Product Info & Actions -->
                        <div class="space-y-6">
                            <div class="hidden lg:block">
                                <h2
                                    class="text-lg font-semibold text-gray-800 mb-4"
                                >
                                    Product Information
                                </h2>
                            </div>

                            <!-- Brand & Category Tags -->
                            <div class="flex flex-wrap items-center gap-2">
                                <span
                                    class="bg-gradient-to-r from-orange-500 to-orange-600 text-white px-3 py-1 rounded-full text-xs font-medium"
                                >
                                    {{ product.brand || "Generic Brand" }}
                                </span>
                                <span
                                    class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs font-medium"
                                >
                                    {{ product.category?.name || "Medication" }}
                                </span>
                            </div>

                            <!-- Product Name & Description -->
                            <div class="space-y-3">
                                <h1
                                    class="text-2xl lg:text-3xl font-bold text-gray-800 leading-tight"
                                >
                                    {{ product.name }}
                                </h1>
                                <p
                                    class="text-gray-600 leading-relaxed text-base"
                                >
                                    {{
                                        product.description ||
                                        "No description available for this medication."
                                    }}
                                </p>
                            </div>

                            <!-- Price -->
                            <div class="py-4 border-y border-gray-200">
                                <div class="flex items-baseline gap-2">
                                    <span
                                        class="text-xl font-semibold text-orange-600"
                                    >
                                        ₵{{ product.price }}
                                    </span>
                                    <span class="text-gray-500 text-sm"
                                        >per unit</span
                                    >
                                </div>
                                <p
                                    v-if="
                                        product.stock < 10 && product.stock > 0
                                    "
                                    class="text-amber-600 text-sm mt-1 font-medium"
                                >
                                    ⚠️ Limited stock available
                                </p>
                            </div>

                            <!-- Add to Cart Section -->
                            <div class="space-y-4" v-if="product.stock > 0">
                                <div v-if="!isInCart" class="space-y-3">
                                    <button
                                        @click="handleAddOrIncrement"
                                        class="w-full lg:w-auto px-8 py-3 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white rounded-xl font-semibold transition-all duration-200 shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
                                        :disabled="cartLoading[product.id]"
                                    >
                                        <span v-if="cartLoading[product.id]">
                                            <i
                                                class="pi pi-spinner pi-spin"
                                            ></i>
                                            <span class="ml-2">Adding...</span>
                                        </span>
                                        <span v-else class="flex gap-2">
                                            <i class="pi pi-shopping-cart"></i>
                                            <span>Add to Cart</span>
                                        </span>
                                    </button>
                                </div>

                                <div v-else class="space-y-3">
                                    <p
                                        class="text-sm text-gray-600 font-medium"
                                    >
                                        Quantity in cart:
                                    </p>
                                    <div class="flex items-center gap-4">
                                        <div
                                            class="flex items-center bg-white border-2 border-orange-200 rounded-xl shadow-sm"
                                        >
                                            <button
                                                @click="handleDecrement"
                                                class="p-3 text-orange-600 hover:bg-orange-50 rounded-l-xl transition-colors"
                                                title="Decrease quantity"
                                            >
                                                <i
                                                    class="pi pi-minus text-sm font-bold"
                                                ></i>
                                            </button>
                                            <span
                                                class="px-6 py-3 font-bold text-lg text-gray-700 border-x border-orange-200"
                                            >
                                                {{ getProductQuantity }}
                                            </span>
                                            <button
                                                @click="handleAddOrIncrement"
                                                class="p-3 text-orange-600 hover:bg-orange-50 rounded-r-xl transition-colors"
                                                title="Increase quantity"
                                            >
                                                <i
                                                    class="pi pi-plus text-sm font-bold"
                                                ></i>
                                            </button>
                                        </div>
                                        <button
                                            @click="() => router.push('/carts')"
                                            class="px-6 py-3 md:py-4 text-xs md:text-base bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white rounded-xl font-medium transition-all duration-200 shadow-md"
                                        >
                                            View Cart
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <!-- Out of Stock -->
                            <div v-else class="py-4">
                                <div
                                    class="bg-red-50 border border-red-200 rounded-xl p-4 text-center"
                                >
                                    <i
                                        class="pi pi-exclamation-triangle text-red-500 text-xl mb-2"
                                    ></i>
                                    <p class="text-red-700 font-medium">
                                        This item is currently out of stock
                                    </p>
                                    <p class="text-red-600 text-sm mt-1">
                                        Check back later for availability
                                    </p>
                                </div>
                            </div>

                            <!-- Additional Info -->
                            <div
                                class="space-y-4 pt-4 border-t border-gray-200"
                            >
                                <!-- Delivery Info -->
                                <div
                                    class="bg-blue-50 border border-blue-200 rounded-lg p-4"
                                >
                                    <div class="flex items-center gap-2 mb-2">
                                        <i
                                            class="pi pi-truck text-blue-600"
                                        ></i>
                                        <span class="font-medium text-blue-900"
                                            >Delivery Information</span
                                        >
                                    </div>
                                    <p class="text-blue-700 text-sm">
                                        Standard delivery within Kumasi is ₵15.
                                    </p>
                                </div>

                                <!-- Ratings (placeholder) -->
                                <div class="flex items-center gap-2">
                                    <div
                                        class="flex items-center text-yellow-500"
                                    >
                                        <i
                                            class="pi pi-star-fill"
                                            v-for="n in 4"
                                            :key="n"
                                        ></i>
                                        <i class="pi pi-star text-gray-300"></i>
                                    </div>
                                    <span class="text-gray-600 text-sm">
                                        ({{ product.ratings || 12 }} verified
                                        ratings)
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Error State -->
        <div v-else class="flex items-center justify-center min-h-screen">
            <div class="text-center max-w-md mx-auto px-4">
                <div
                    class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6"
                >
                    <i
                        class="pi pi-exclamation-triangle text-3xl text-gray-400"
                    ></i>
                </div>
                <h3 class="text-xl font-semibold text-gray-700 mb-3">
                    Product Not Found
                </h3>
                <p class="text-gray-500 mb-6">
                    The product you're looking for doesn't exist or has been
                    removed.
                </p>
                <button
                    @click="$router.push('/')"
                    class="px-6 py-3 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg font-medium hover:from-orange-600 hover:to-orange-700 transition-all duration-200 shadow-md"
                >
                    Browse Products
                </button>
            </div>
        </div>
    </div>
</template>
