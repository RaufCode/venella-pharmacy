<script setup>
    import { onMounted } from "vue";
    import { useCartStore } from "@/stores/cartStore";
    import { storeToRefs } from "pinia";
    import { useRouter } from "vue-router";

    const router = useRouter();
    const cartStore = useCartStore();
    const { carts, isLoading, error, subtotal } = storeToRefs(cartStore);

    const {
        fetchCartItems,
        deleteItem,
        updateQuantity,
        getItemTotal,
        getImage,
        truncate,
        clearError,
    } = cartStore;

    onMounted(() => {
        fetchCartItems();
    });

    const goBack = () => {
        if (window.history.length > 1) {
            router.back();
        } else {
            router.push("/");
        }
    };

    const onErrorImage = (event) => {
        event.target.src = "/placeholder-image.jpg";
    };

    const onDecreaseQty = (id, qty) => {
        if (qty > 1) updateQuantity(id, qty - 1);
    };

    const onIncreaseQty = (id, qty) => {
        updateQuantity(id, qty + 1);
    };

    const proceedCheckout = () => {
        if (carts.value.length === 0) return;
        cartStore.checkout(); // Assuming this is defined in your store
    };
</script>

<template>
    <div class="min-h-screen flex flex-col bg-gray-50">
        <!-- Header -->
        <header
            class="bg-gray-900 text-white p-4 flex items-center gap-4 sticky top-0 z-50"
        >
            <button @click="goBack" class="hover:text-orange-400 transition">
                <i class="pi pi-arrow-left text-lg"></i>
            </button>
            <h1 class="text-base md:text-xl font-semibold">Your Cart</h1>
        </header>

        <!-- Error Message -->
        <div
            v-if="error"
            class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 mx-4 mt-4 rounded"
        >
            {{ error }}
            <button @click="clearError" class="float-right font-bold">
                &times;
            </button>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="flex justify-center items-center py-10">
            <div class="text-gray-600">Loading cart items...</div>
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
                            class="font-medium text-gray-800 text-sm md:text-base"
                        >
                            {{ truncate(cart.product?.name, 25) }}
                        </h2>
                        <p class="text-xs md:text-sm text-gray-500 mt-1">
                            {{
                                truncate(
                                    cart.product?.description ||
                                        cart.product?.name,
                                    40
                                )
                            }}
                        </p>

                        <div class="mt-2 flex items-center gap-2 md:gap-3">
                            <button
                                @click="onDecreaseQty(cart.id, cart.quantity)"
                                :disabled="cart.quantity <= 1"
                                class="bg-gray-200 px-2 py-1 rounded hover:bg-gray-300 text-xs md:text-base disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                −
                            </button>
                            <span
                                class="font-semibold text-sm md:text-base min-w-[2rem] text-center"
                            >
                                {{ cart.quantity || 0 }}
                            </span>
                            <button
                                @click="onIncreaseQty(cart.id, cart.quantity)"
                                class="bg-gray-200 px-2 py-1 rounded hover:bg-gray-300 text-xs md:text-base"
                            >
                                +
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
                            <i class="pi pi-trash"></i>
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
                    <span class="text-gray-600 text-sm">
                        Subtotal ({{ carts.length }} items)
                    </span>
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
