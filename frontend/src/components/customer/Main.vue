<script setup>
    import { onMounted, ref, computed } from "vue";
    import { useRouter } from "vue-router";
    import { useCartStore } from "@/stores/cartStore";
    import { useMedStore } from "@/stores/medStore";
    import { useAuthStore } from "@/stores/auth";
    import { storeToRefs } from "pinia";

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

    // Show 8 products initially and load more on "See More"
    const visibleCount = ref(4);

    const visibleProducts = computed(() =>
        products.value.slice(0, visibleCount.value)
    );

    const showMore = () => {
        visibleCount.value += 4;
    };

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
        // Allow all users to navigate to the product detail page
        router.push(`/product/${productId}`);
    };
</script>

<template>
    <main class="min-h-screen bg-gray-50">
        <section class="container mx-auto px-4 lg:px-10 pt-32 pb-10">
            <h1 class="text-2xl font-semibold mb-6">Products Available</h1>

            <!-- Loading Spinner -->
            <div
                v-if="isLoadingProducts"
                class="flex justify-center items-center py-10"
            >
                <i class="pi pi-spinner pi-spin text-3xl text-orange-600"></i>
                <span class="ml-3 text-gray-600">Loading products...</span>
            </div>

            <!-- Product Grid -->
            <div
                v-else
                class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6"
            >
                <article
                    v-for="product in visibleProducts"
                    :key="product.id"
                    @click="() => navigateToProduct(product.id)"
                    class="bg-white rounded-2xl border shadow-sm hover:shadow-md transition p-4 flex flex-col cursor-pointer"
                >
                    <!-- Product Image and Info -->
                    <div
                        class="h-40 bg-gray-100 rounded-xl overflow-hidden mb-3"
                    >
                        <img
                            :src="`https://techrems.pythonanywhere.com${product.images?.[0]?.image}`"
                            :alt="product.name"
                            class="w-full h-full object-cover"
                            @error="
                                $event.target.src = '/placeholder-image.jpg'
                            "
                        />
                    </div>
                    <h3
                        class="font-semibold text-lg text-gray-800 truncate mb-1"
                    >
                        {{ product.name }}
                    </h3>
                    <p class="text-gray-600 text-sm flex-grow truncate">
                        {{ product.description || "No description available" }}
                    </p>
                    <!-- Price & Cart Button -->
                    <div class="mt-4 flex justify-between items-center">
                        <p class="text-orange-600 font-bold text-lg">
                            ₵{{ product.price }}
                        </p>
                        <div class="relative flex items-center">
                            <template v-if="isCartLoaded">
                                <template v-if="!isInCart(product.id)">
                                    <!-- Show Add to Cart Button Always -->
                                    <button
                                        class="py-2 px-3 rounded-full bg-orange-600 flex items-center justify-center text-white"
                                        :disabled="
                                            isAuthenticated &&
                                            isAddingToCart(product.id)
                                        "
                                        @click.stop="
                                            () =>
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
                                                class="pi pi-spinner pi-spin text-white"
                                                style="font-size: 1.2rem"
                                            ></i>
                                        </span>
                                        <span v-else>
                                            <i class="pi pi-shopping-cart"></i>
                                        </span>
                                    </button>
                                </template>

                                <!-- Quantity Controls for Authenticated -->
                                <template v-else>
                                    <div
                                        v-if="isAuthenticated"
                                        class="flex items-center relative"
                                    >
                                        <button
                                            type="button"
                                            @click.stop="
                                                cartStore.decrementQuantity(
                                                    product.id
                                                )
                                            "
                                            class="bg-orange-700 text-white rounded-full w-6 h-6 flex items-center justify-center"
                                            title="Decrease quantity"
                                        >
                                            &minus;
                                        </button>
                                        <span
                                            class="mx-4 font-semibold select-none"
                                        >
                                            {{ getProductQuantity(product.id) }}
                                        </span>
                                        <button
                                            type="button"
                                            @click.stop="
                                                cartStore.incrementQuantity(
                                                    product.id
                                                )
                                            "
                                            class="bg-orange-700 text-white rounded-full w-6 h-6 flex items-center justify-center"
                                            title="Increase quantity"
                                        >
                                            +
                                        </button>
                                    </div>
                                </template>
                            </template>
                            <template v-else>
                                <div
                                    class="w-24 h-8 bg-gray-200 rounded animate-pulse"
                                ></div>
                            </template>
                        </div>
                    </div>
                </article>
            </div>

            <!-- See More Button -->
            <div
                v-if="visibleCount < products.length"
                class="flex justify-center mt-8"
            >
                <button
                    @click="showMore"
                    class="bg-orange-600 hover:bg-orange-700 text-white text-sm px-6 py-2 rounded-full shadow transition"
                >
                    See More
                </button>
            </div>
        </section>
    </main>
</template>
