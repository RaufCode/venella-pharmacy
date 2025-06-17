<script setup>
    import { onMounted, ref, computed } from "vue";
    import { useRouter } from "vue-router";
    import { useCartStore } from "@/stores/cartStore";
    import { useMedStore } from "@/stores/medStore";
    import { useAuthStore } from "@/stores/auth";
    import { storeToRefs } from "pinia";
    import Spinner from "../ui/Spinner.vue";

    const router = useRouter();

    // Pinia Stores
    const cartStore = useCartStore();
    const medStore = useMedStore();
    const authStore = useAuthStore();

    // Store Refs
    const { carts, cartLoading } = storeToRefs(cartStore);
    const { products } = storeToRefs(medStore);
    const isAuthenticated = computed(() => authStore.isAuthenticated);

    // State
    const isLoadingProducts = ref(false);
    const isCartLoaded = ref(false);

    // Lifecycle
    onMounted(async () => {
        isLoadingProducts.value = true;
        await medStore.fetchProducts();
        isLoadingProducts.value = false;

        if (isAuthenticated.value) {
            await cartStore.fetchCartItems();
        }

        isCartLoaded.value = true;
    });

    // Cart Helpers
    const isInCart = (productId) => {
        const item = carts.value.find((item) => item.product?.id === productId);
        return item && item.quantity > 0;
    };

    const getProductQuantity = (productId) => {
        if (!isCartLoaded.value) return 0;
        const item = carts.value.find((item) => item.product?.id === productId);
        return item ? item.quantity : 0;
    };

    const isAddingToCart = (productId) =>
        isAuthenticated.value &&
        cartLoading.value[productId] &&
        !isInCart(productId);

    const handleAddOrIncrement = async (productId) => {
        if (!isAuthenticated.value) {
            alert("Please log in to add products to cart.");
            return;
        }

        if (!isInCart(productId)) {
            await cartStore.addToCart(productId);
        } else {
            await cartStore.incrementQuantity(productId);
        }
    };

    const navigateToProduct = (productId) => {
        router.push(`/product/${productId}`);
    };
</script>

<template>
    <main
        class="min-h-screen bg-gradient-to-br from-gray-50 to-white pt-40 pb-10 md:pt-32"
    >
        <section class="container mx-auto px-4 md:px-10">
            <!-- Header Section -->
            <div class="text-center mb-12">
                <h1 class="text-2xl font-styleScript text-orange-600">
                    Available Medications
                </h1>
                <p
                    class="text-gray-600 max-w-2xl mx-auto mt-2 text-justify text-base md:text-lg md:text-center"
                >
                    Browse through our carefully curated selection of quality
                    medications and health products
                </p>
            </div>

            <Spinner v-if="isLoadingProducts" />

            <!-- Products Grid -->
            <div
                v-else-if="products.length > 0"
                class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
            >
                <article
                    v-for="product in products"
                    :key="product.id"
                    @click="() => navigateToProduct(product.id)"
                    class="group bg-white rounded-2xl hover:shadow-xl transition-all duration-300 p-4 flex flex-col cursor-pointer border border-gray-100 hover:border-orange-200 hover:-translate-y-1"
                >
                    <!-- Product Image -->
                    <div
                        class="relative h-48 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl overflow-hidden mb-2"
                    >
                        <img
                            :src="`https://techrems.pythonanywhere.com${product.images?.[0]?.image}`"
                            :alt="product.name"
                            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                            @error="
                                $event.target.src = '/placeholder-image.jpg'
                            "
                        />
                        <!-- Stock indicator -->
                        <div class="absolute top-3 left-3">
                            <span
                                :class="[
                                    'px-2 py-1 text-xs font-medium rounded-full',
                                    product.stock > 10
                                        ? 'bg-green-100 text-green-700'
                                        : product.stock > 0
                                        ? 'bg-yellow-100 text-yellow-700'
                                        : 'bg-red-100 text-red-700',
                                ]"
                            >
                                {{
                                    product.stock > 0
                                        ? `${product.stock} left`
                                        : "Out of stock"
                                }}
                            </span>
                        </div>
                    </div>

                    <!-- Brand Badge -->
                    <div class="mb-1">
                        <span
                            class="inline-block bg-gradient-to-r from-orange-500 to-orange-600 text-white px-2 py-1 text-[10px] font-medium rounded-full"
                        >
                            {{ product.brand || "Generic" }}
                        </span>
                    </div>

                    <!-- Product Info -->
                    <div class="flex-grow">
                        <h3
                            class="text-gray-700 font-semibold mb-1 line-clamp-2 group-hover:text-orange-600 transition-colors"
                        >
                            {{ product.name }}
                        </h3>
                        <p
                            class="text-gray-600 text-sm leading-relaxed mb-2 line-clamp-2"
                        >
                            {{
                                product.description ||
                                "High-quality medication for your health needs"
                            }}
                        </p>
                    </div>

                    <!-- Price and Actions -->
                    <div
                        class="flex justify-between items-center mt-auto pt-2 border-t border-gray-100"
                    >
                        <div>
                            <p class="font-semibold text-orange-600">
                                ₵{{ product.price }}
                            </p>
                            <p class="text-xs text-gray-500">per unit</p>
                        </div>

                        <div class="flex items-center" @click.stop>
                            <template v-if="isCartLoaded && product.stock > 0">
                                <template v-if="!isInCart(product.id)">
                                    <button
                                        class="p-4 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white rounded-full font-medium transition-all duration-200 shadow-md flex items-center gap-2"
                                        :disabled="
                                            isAuthenticated &&
                                            isAddingToCart(product.id)
                                        "
                                        @click="
                                            handleAddOrIncrement(product.id)
                                        "
                                        title="Add to cart"
                                    >
                                        <span
                                            v-if="
                                                isAuthenticated &&
                                                isAddingToCart(product.id)
                                            "
                                        >
                                            <i
                                                class="pi pi-spinner pi-spin"
                                            ></i>
                                        </span>
                                        <span
                                            v-else
                                            class="flex items-center gap-2"
                                        >
                                            <i class="pi pi-shopping-cart"></i>
                                        </span>
                                    </button>
                                </template>

                                <template v-else>
                                    <div
                                        v-if="isAuthenticated"
                                        class="flex items-center bg-white rounded-lg border-2 border-orange-200 shadow-sm"
                                    >
                                        <button
                                            type="button"
                                            @click="
                                                cartStore.decrementQuantity(
                                                    product.id
                                                )
                                            "
                                            class="p-2 text-orange-600 hover:bg-orange-50 rounded-l-lg transition-colors"
                                            title="Decrease quantity"
                                        >
                                            <i class="pi pi-minus text-sm"></i>
                                        </button>
                                        <span
                                            class="px-3 py-2 font-bold text-gray-700 border-x border-orange-200"
                                        >
                                            {{ getProductQuantity(product.id) }}
                                        </span>
                                        <button
                                            type="button"
                                            @click="
                                                cartStore.incrementQuantity(
                                                    product.id
                                                )
                                            "
                                            class="p-2 text-orange-600 hover:bg-orange-50 rounded-r-lg transition-colors"
                                            title="Increase quantity"
                                        >
                                            <i class="pi pi-plus text-sm"></i>
                                        </button>
                                    </div>
                                </template>
                            </template>

                            <template v-else-if="product.stock === 0">
                                <span
                                    class="px-4 py-2 bg-gray-100 text-gray-500 rounded-lg font-medium cursor-not-allowed"
                                >
                                    Out of Stock
                                </span>
                            </template>

                            <template v-else>
                                <div
                                    class="w-20 h-8 bg-gray-200 rounded-lg animate-pulse"
                                ></div>
                            </template>
                        </div>
                    </div>
                </article>
            </div>

            <!-- Empty State -->
            <div v-else class="text-center py-20">
                <div class="max-w-md mx-auto">
                    <div
                        class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6"
                    >
                        <i class="pi pi-box text-3xl text-gray-400"></i>
                    </div>
                    <h3 class="text-xl font-semibold text-gray-700 mb-3">
                        No Medications Available
                    </h3>
                    <p class="text-gray-500 mb-6">
                        We're currently updating our inventory. Please check
                        back soon for available medications.
                    </p>
                    <button
                        @click="() => window.location.reload()"
                        class="px-6 py-3 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg font-medium hover:from-orange-600 hover:to-orange-700 transition-all duration-200 shadow-md"
                    >
                        Refresh Page
                    </button>
                </div>
            </div>
        </section>
    </main>
</template>
