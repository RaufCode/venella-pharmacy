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
    <main class="min-h-screen bg-gray-50">
        <section class="container mx-auto px-4 lg:px-10 pt-32 pb-10">
            <h1 class="text-xl font-semibold text-gray-700 mb-6">
                Products Available
            </h1>

            <Spinner v-if="isLoadingProducts" />

            <div
                v-else
                class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4"
            >
                <article
                    v-for="product in products"
                    :key="product.id"
                    @click="() => navigateToProduct(product.id)"
                    class="bg-white rounded-2xl hover:shadow-md transition p-4 flex flex-col cursor-pointer"
                >
                    <div class="h-40 bg-gray-100 overflow-hidden mb-3">
                        <img
                            :src="`https://techrems.pythonanywhere.com${product.images?.[0]?.image}`"
                            :alt="product.name"
                            class="w-full h-full object-cover"
                            @error="
                                $event.target.src = '/placeholder-image.jpg'
                            "
                        />
                    </div>

                    <p
                        class="text-xs bg-orange-600 px-3 py-1 mb-2 text-white rounded-full w-max"
                    >
                        {{ product.brand || "No brand name" }}
                    </p>

                    <h3
                        class="font-semibold text-sm text-gray-800 truncate mb-1"
                    >
                        {{ product.name }}
                    </h3>
                    <p
                        class="text-gray-600 text-xs font-medium flex-grow truncate"
                    >
                        {{ product.description || "No description available" }}
                    </p>

                    <div class="mt-4 flex justify-between items-center">
                        <p class="text-orange-600 font-bold text-lg">
                            ₵{{ product.price }}
                        </p>
                        <div class="relative flex items-center">
                            <template v-if="isCartLoaded">
                                <template v-if="!isInCart(product.id)">
                                    <button
                                        class="py-2 px-3 rounded-full bg-green-600 flex items-center justify-center text-white"
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
                                            class="bg-orange-600 text-white rounded-full w-6 h-6 flex items-center justify-center"
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
                                            class="bg-orange-600 text-white rounded-full w-6 h-6 flex items-center justify-center"
                                            title="Increase quantity"
                                        >
                                            +
                                        </button>
                                    </div>
                                </template>
                            </template>

                            <template v-else>
                                <Spinner />
                            </template>
                        </div>
                    </div>
                </article>
            </div>
        </section>
    </main>
</template>
