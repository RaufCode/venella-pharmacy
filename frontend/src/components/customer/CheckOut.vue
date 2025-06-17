<script setup>
    import { ref, computed, onMounted } from "vue";
    import router from "@/router";
    import { useCartStore } from "@/stores/cartStore";
    import { useOrderStore } from "@/stores/orderStore";
    import { ArrowLeft } from "lucide-vue-next";

    const cartStore = useCartStore();
    const orderStore = useOrderStore();

    const isLoading = ref(false);

    onMounted(() => {
        cartStore.fetchCartItems();
    });

    const delivery = 15;

    const totalWithDelivery = computed(() => {
        const subtotal = parseFloat(cartStore.subtotal) || 0;
        return (subtotal + delivery).toFixed(2);
    });

    const form = ref({
        name: "",
        phone: "",
        address: "",
    });

    const isFormValid = computed(() => {
        return (
            form.value.name.trim() !== "" &&
            form.value.phone.trim() !== "" &&
            form.value.address.trim() !== ""
        );
    });

    const placeOrder = async () => {
        if (!isFormValid.value) {
            alert("Please fill in all required fields.");
            return;
        }

        if (!cartStore.carts || cartStore.carts.length === 0) {
            alert("Your cart is empty.");
            return;
        }

        isLoading.value = true;
        orderStore.clearMessages();

        try {
            const cartId = cartStore.carts[0]?.cart;

            if (!cartId) {
                throw new Error("Cart ID not available.");
            }

            const payload = {
                cart: cartId,
                shipping_address: form.value.address.trim(),
                customer_name: form.value.name.trim(),
                customer_phone: form.value.phone.trim(),
            };

            await orderStore.createOrder(payload);

            if (orderStore.error) {
                throw new Error(orderStore.error);
            }

            cartStore.carts = [];
            form.value = { name: "", phone: "", address: "" };

            alert(
                "Order placed successfully! You will be redirected to the home page."
            );
            router.push("/");
        } catch (error) {
            console.error("Order failed:", error);
            alert(error.message || "Failed to place order. Please try again.");
        } finally {
            isLoading.value = false;
        }
    };

    const goBack = () => {
        if (window.history.length > 1) {
            router.back();
        } else {
            router.push("/");
        }
    };
</script>

<template>
    <div
        class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-orange-50"
    >
        <!-- Header -->
        <div
            class="sticky top-0 z-10 bg-white/80 backdrop-blur-sm border-b border-gray-200"
        >
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex items-center justify-between h-16">
                    <button
                        @click="goBack"
                        class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-gray-400 transition-all duration-200 shadow-sm"
                    >
                        <ArrowLeft class="w-4 h-4" />
                        Back
                    </button>
                    <h1
                        class="text-2xl font-styleScript bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent"
                    >
                        Checkout
                    </h1>
                </div>
            </div>
        </div>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Loading State -->
            <div v-if="cartStore.isLoading" class="text-center py-16">
                <div
                    class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-orange-100 to-red-100 rounded-full mb-4"
                >
                    <div
                        class="w-8 h-8 border-4 border-orange-200 border-t-orange-600 rounded-full animate-spin"
                    ></div>
                </div>
                <p class="text-gray-600 font-medium">Loading your cart...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="cartStore.error" class="max-w-md mx-auto">
                <div
                    class="bg-red-50 border border-red-200 rounded-xl p-6 text-center"
                >
                    <div
                        class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4"
                    >
                        <svg
                            class="w-6 h-6 text-red-600"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16c-.77.833.192 2.5 1.732 2.5z"
                            ></path>
                        </svg>
                    </div>
                    <h3 class="text-lg font-semibold text-red-800 mb-2">
                        Oops! Something went wrong
                    </h3>
                    <p class="text-red-600 mb-4">{{ cartStore.error }}</p>
                    <button
                        @click="cartStore.fetchCartItems()"
                        class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
                    >
                        Try Again
                    </button>
                </div>
            </div>

            <!-- Empty Cart State -->
            <div
                v-else-if="!cartStore.carts || cartStore.carts.length === 0"
                class="text-center py-16"
            >
                <div class="max-w-md mx-auto">
                    <div
                        class="w-24 h-24 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto mb-6"
                    >
                        <svg
                            class="w-12 h-12 text-gray-400"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.293 2.293A1 1 0 005 16h12M9 19.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM20.5 19.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z"
                            ></path>
                        </svg>
                    </div>
                    <h3 class="text-2xl font-bold text-gray-800 mb-4">
                        Your cart is empty
                    </h3>
                    <p class="text-gray-600 mb-8">
                        Add some products to your cart to continue with checkout
                    </p>
                </div>
            </div>

            <!-- Checkout Form -->
            <div v-else class="grid lg:grid-cols-3 gap-8">
                <!-- Order Summary -->
                <div class="lg:col-span-2">
                    <div
                        class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden"
                    >
                        <div
                            class="bg-gradient-to-r from-green-50 to-emerald-50 px-6 py-4 border-b border-green-100"
                        >
                            <h2
                                class="text-xl font-semibold text-green-700 flex items-center gap-2"
                            >
                                <svg
                                    class="w-6 h-6"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                                    ></path>
                                </svg>
                                Order Summary
                            </h2>
                            <p class="text-green-600 text-sm mt-1">
                                Review your items before checkout
                            </p>
                        </div>

                        <div class="p-6">
                            <div
                                class="space-y-4 max-h-96 overflow-y-auto overscroll-contain"
                            >
                                <div
                                    v-for="item in cartStore.carts"
                                    :key="item.id"
                                    class="flex items-start gap-4 p-4 bg-gray-50 rounded-xl border border-gray-100 hover:border-gray-200 transition-colors"
                                >
                                    <div
                                        class="w-16 h-16 bg-gradient-to-br from-orange-100 to-red-100 rounded-lg flex items-center justify-center flex-shrink-0"
                                    >
                                        <svg
                                            class="w-8 h-8 text-orange-600"
                                            fill="none"
                                            stroke="currentColor"
                                            viewBox="0 0 24 24"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
                                            ></path>
                                        </svg>
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <h3
                                            class="font-semibold text-gray-800 line-clamp-1"
                                        >
                                            {{
                                                item.product?.name ||
                                                "Unknown Product"
                                            }}
                                        </h3>
                                        <p
                                            class="text-sm text-gray-600 line-clamp-2 mt-1"
                                        >
                                            {{
                                                item.product?.description ||
                                                "No description available"
                                            }}
                                        </p>
                                        <div
                                            class="flex items-center justify-between mt-3"
                                        >
                                            <span class="text-sm text-gray-500"
                                                >Qty:
                                                {{ item.quantity || 0 }}</span
                                            >
                                            <span
                                                class="font-bold text-green-600"
                                                >₵{{
                                                    item.product?.price || 0
                                                }}</span
                                            >
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Pricing Breakdown -->
                            <div
                                class="border-t border-gray-200 mt-6 pt-6 space-y-3"
                            >
                                <div class="flex justify-between text-gray-600">
                                    <span>Subtotal</span>
                                    <span class="font-medium"
                                        >₵{{ cartStore.subtotal }}</span
                                    >
                                </div>
                                <div class="flex justify-between text-gray-600">
                                    <span>Delivery Fee</span>
                                    <span class="font-medium"
                                        >₵{{ delivery }}</span
                                    >
                                </div>
                                <div
                                    class="flex justify-between text-lg font-bold text-gray-800 pt-3 border-t border-gray-200"
                                >
                                    <span>Total</span>
                                    <span class="text-green-600"
                                        >₵{{ totalWithDelivery }}</span
                                    >
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Delivery Form -->
                <div class="lg:col-span-1">
                    <div
                        class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden sticky top-24"
                    >
                        <div
                            class="bg-gradient-to-r from-orange-50 to-red-50 px-6 py-4 border-b border-orange-100"
                        >
                            <h2
                                class="text-xl font-semibold text-orange-700 flex items-center gap-2"
                            >
                                <svg
                                    class="w-6 h-6"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                                    ></path>
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                                    ></path>
                                </svg>
                                Delivery Details
                            </h2>
                            <p class="text-orange-600 text-sm mt-1">
                                Where should we deliver your order?
                            </p>
                        </div>

                        <div class="p-6">
                            <!-- Order Error -->
                            <div
                                v-if="orderStore.error"
                                class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl"
                            >
                                <div class="flex items-start gap-3">
                                    <svg
                                        class="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0"
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16c-.77.833.192 2.5 1.732 2.5z"
                                        ></path>
                                    </svg>
                                    <p class="text-red-700 text-sm">
                                        {{ orderStore.error }}
                                    </p>
                                </div>
                            </div>

                            <form
                                @submit.prevent="placeOrder"
                                class="space-y-6 text-sm"
                            >
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700 mb-2"
                                    >
                                        Full Name *
                                    </label>
                                    <input
                                        type="text"
                                        v-model="form.name"
                                        required
                                        :disabled="
                                            isLoading || orderStore.loading
                                        "
                                        class="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-all duration-200 disabled:bg-gray-100 disabled:cursor-not-allowed"
                                        placeholder="Enter your full name"
                                    />
                                </div>

                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700 mb-2"
                                    >
                                        Phone Number *
                                    </label>
                                    <input
                                        type="tel"
                                        v-model="form.phone"
                                        required
                                        :disabled="
                                            isLoading || orderStore.loading
                                        "
                                        class="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-all duration-200 disabled:bg-gray-100 disabled:cursor-not-allowed"
                                        placeholder="Enter your phone number"
                                    />
                                </div>

                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700 mb-2"
                                    >
                                        Delivery Address *
                                    </label>
                                    <textarea
                                        v-model="form.address"
                                        required
                                        rows="4"
                                        :disabled="
                                            isLoading || orderStore.loading
                                        "
                                        class="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-all duration-200 resize-none disabled:bg-gray-100 disabled:cursor-not-allowed"
                                        placeholder="Enter your complete delivery address including landmarks"
                                    ></textarea>
                                </div>

                                <button
                                    type="submit"
                                    :disabled="
                                        isLoading ||
                                        orderStore.loading ||
                                        !isFormValid
                                    "
                                    class="w-full bg-gradient-to-r from-orange-600 to-red-600 text-white py-4 px-6 rounded-full font-semibold hover:from-orange-700 hover:to-red-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transition-all duration-200 shadow hover:shadow-xl transform hover:scale-[1.02] disabled:transform-none disabled:shadow-md"
                                >
                                    <span
                                        v-if="isLoading || orderStore.loading"
                                        class="flex items-center justify-center gap-2"
                                    >
                                        <div
                                            class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"
                                        ></div>
                                        Placing Order...
                                    </span>
                                    <span
                                        v-else
                                        class="flex items-center justify-center gap-2"
                                    >
                                        <svg
                                            class="w-5 h-5"
                                            fill="none"
                                            stroke="currentColor"
                                            viewBox="0 0 24 24"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M5 13l4 4L19 7"
                                            ></path>
                                        </svg>
                                        Confirm Order
                                    </span>
                                </button>

                                <p
                                    class="text-xs text-gray-500 text-center mt-4"
                                >
                                    By placing this order, you agree to our
                                    terms and conditions
                                </p>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
