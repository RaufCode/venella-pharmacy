<script setup>
    import { onMounted } from "vue";
    import { useCartStore } from "@/stores/cartStore";
    import { storeToRefs } from "pinia";
    import { useRouter } from "vue-router";
    import Spinner from "../ui/Spinner.vue";
    import { useToast } from "vue-toastification";
    import { Trash2, Plus, Minus, ArrowLeft } from "lucide-vue-next";

    const router = useRouter();
    const toast = useToast();
    const cartStore = useCartStore();
    const { carts, isLoading, error, subtotal, stockAlerts } =
        storeToRefs(cartStore);

    const {
        fetchCartItems,
        deleteItem,
        updateQuantity,
        clearStockAlert,
        checkProductStock,
        showStockAlert,
    } = cartStore;

    const goBack = () => router.back();

    onMounted(fetchCartItems);

    const truncate = (text, len = 60) =>
        text?.length > len ? text.slice(0, len) + "..." : text || "";

    const getItemTotal = (item) =>
        ((+item?.product?.price || 0) * (+item?.quantity || 0)).toFixed(2);

    const getStockAlert = (id) => stockAlerts.value[id] || null;

    const onErrorImage = (e) => (e.target.src = "/placeholder-image.jpg");

    const onDecreaseQty = (id, qty) => qty > 1 && updateQuantity(id, qty - 1);

    const onIncreaseQty = async (item) => {
        const stock = await checkProductStock(item.product.id);
        if (item.quantity >= stock) {
            toast.error(`Only ${stock} items available.`);
        } else {
            updateQuantity(item.id, item.quantity + 1);
        }
    };

    const proceedCheckout = () => {
        if (carts.value.length > 0) router.push("/checkout");
    };

    const clearError = () => (cartStore.error = null);

    // Utility to get product image
    const getImage = (product) => {
        return product?.images?.[0]?.image
            ? `https://techrems.pythonanywhere.com${product.images[0].image}`
            : "/placeholder-image.jpg";
    };
</script>

<template>
    <div class="min-h-screen flex flex-col bg-gray-50">
        <!-- Header -->
        <header
            class="bg-white border-b border-gray-200 p-4 flex shadow-sm items-center justify-between gap-4 sticky top-0 z-50"
        >
            <div class="flex items-center gap-3">
                <div
                    class="w-8 h-8 bg-gradient-to-br from-orange-500 to-orange-600 rounded-full flex items-center justify-center"
                >
                    <i class="pi pi-shopping-cart text-white text-sm"></i>
                </div>
                <h1
                    class="text-gray-700 text-2xl font-styleScript flex items-center"
                >
                    Carts
                    <span
                        v-if="carts.length > 0"
                        class="text-orange-600 font-normal text-sm ml-2"
                    >
                        ({{ carts.length }} item{{
                            carts.length !== 1 ? "s" : ""
                        }})
                    </span>
                </h1>
            </div>
            <button
                @click="goBack"
                class="px-4 py-2 bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white rounded-lg flex items-center gap-2 font-medium transition-all duration-200 shadow-md"
            >
                <ArrowLeft class="w-4 h-4" />
                <span class="hidden sm:inline">Back</span>
            </button>
        </header>
        <!-- Loading Spinner -->
        <div v-if="isLoading" class="flex justify-center items-center py-20">
            <Spinner />
        </div>

        <!-- Main Content -->
        <main
            v-else
            class="flex flex-col lg:flex-row gap-4 p-4 md:p-6 flex-grow container mx-auto"
        >
            <!-- Cart Items -->
            <section class="flex-1 space-y-3 md:space-y-4">
                <div
                    v-for="cart in carts"
                    :key="cart.id"
                    class="bg-white rounded-lg shadow-md p-3 md:p-4 flex items-center gap-3 md:gap-4"
                >
                    <img
                        :src="getImage(cart.product)"
                        :alt="cart.product?.name || 'Product image'"
                        class="w-14 h-14 md:w-20 md:h-20 object-cover rounded-md"
                        @error="onErrorImage"
                    />

                    <div class="flex-1">
                        <h2
                            class="font-medium text-gray-800 text-sm md:text-base w-20 md:w-auto truncate"
                        >
                            {{ cart.product.name }}
                        </h2>
                        <p
                            class="text-xs md:text-sm text-gray-500 mt-1 max-w-24 md:w-auto truncate"
                        >
                            {{ cart.product.description }}
                        </p>
                        <div class="mt-2 flex items-center gap-2 md:gap-3">
                            <button
                                @click="onDecreaseQty(cart.id, cart.quantity)"
                                :disabled="cart.quantity <= 1"
                                class="bg-gray-200 px-2 py-1 rounded hover:bg-gray-300 text-xs md:text-base disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <Minus class="w-4 h-4" />
                            </button>
                            <span
                                class="font-semibold text-sm md:text-base min-w-[2rem] text-center"
                            >
                                {{ cart.quantity }}
                            </span>
                            <button
                                @click="onIncreaseQty(cart)"
                                class="bg-gray-200 px-2 py-1 rounded hover:bg-gray-300 text-xs md:text-base"
                            >
                                <Plus class="w-4 h-4" />
                            </button>
                        </div>
                    </div>

                    <div
                        class="flex flex-col items-end gap-2 text-xs md:text-base"
                    >
                        <p class="text-orange-600 font-bold">
                            GH₵ {{ getItemTotal(cart) }}
                        </p>
                        <button
                            @click="deleteItem(cart.id)"
                            class="text-red-500 hover:text-red-700 transition-colors"
                            title="Remove item"
                        >
                            <Trash2 class="w-4 h-4" />
                        </button>
                    </div>
                </div>

                <!-- Empty State -->
                <div
                    v-if="carts.length === 0 && !isLoading"
                    class="text-center text-gray-500 mt-10 text-sm md:text-base py-10"
                >
                    <p class="mb-4">
                        <i
                            class="pi pi-shopping-cart text-4xl md:text-6xl text-gray-300"
                        ></i>
                    </p>
                    <h2
                        class="font-medium text-gray-600 text-lg md:text-xl mb-2"
                    >
                        Your cart is empty
                    </h2>
                    <p class="text-gray-500">
                        Items added to the cart will appear here
                    </p>
                </div>
            </section>

            <!-- Cart Summary -->
            <aside
                v-if="carts.length > 0"
                class="w-full lg:w-[300px] bg-white p-4 md:p-6 rounded-lg shadow-md space-y-3 md:space-y-4 h-max text-sm md:text-base lg:text-lg"
            >
                <h2 class="text-base md:text-xl font-semibold text-gray-800">
                    Cart Summary
                </h2>

                <div class="flex justify-between items-center">
                    <span class="text-gray-600 text-sm"
                        >Subtotal ({{ carts.length }} items)</span
                    >
                    <span class="font-semibold text-orange-600"
                        >GH₵ {{ subtotal }}</span
                    >
                </div>

                <p class="text-xs md:text-sm text-gray-500">
                    Delivery fees not included
                </p>

                <div
                    class="bg-green-50 border border-green-200 p-3 rounded-md text-xs md:text-sm lg:text-base text-green-700"
                >
                    <strong>Free delivery</strong> on Express items
                </div>

                <button
                    :disabled="carts.length === 0 || isLoading"
                    @click="proceedCheckout"
                    class="w-full bg-orange-600 text-white py-2 md:py-3 rounded-md font-medium hover:bg-orange-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm md:text-base"
                >
                    Proceed to Checkout
                </button>
            </aside>
        </main>
    </div>
</template>
