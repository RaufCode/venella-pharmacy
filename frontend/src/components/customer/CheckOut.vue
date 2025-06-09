<script setup>
    import { ref, computed, onMounted } from "vue";
    import Btn from "@/components/ui/Btn.vue";
    import router from "@/router";
    import { useCartStore } from "@/stores/cartStore";
    import { useOrderStore } from "@/stores/orderStore";

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
    <div class="h-screen w-full">
        <div
            class="min-h-screen md:flex items-center justify-center bg-gray-100 p-4 mb-0"
        >
            <div
                class="max-w-3xl w-full bg-gray-100 rounded-xl shadow-md overflow-hidden mx-auto"
            >
                <div class="p-2 md:p-6">
                    <button
                        type="button"
                        @click="goBack"
                        aria-label="Go back"
                        class="flex items-center text-gray-600 hover:text-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-600 transition mb-4"
                    >
                        <i class="pi pi-arrow-left mr-2"></i> Go Back
                    </button>

                    <div v-if="cartStore.isLoading" class="text-center py-8">
                        <p class="text-gray-600">Loading cart items...</p>
                    </div>

                    <div
                        v-else-if="cartStore.error"
                        class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded"
                    >
                        {{ cartStore.error }}
                    </div>

                    <div
                        v-else-if="
                            !cartStore.carts || cartStore.carts.length === 0
                        "
                        class="text-center py-8"
                    >
                        <p class="text-gray-600 mb-4">Your cart is empty</p>
                        <button
                            @click="router.push('/')"
                            class="bg-orange-600 text-white px-4 py-2 rounded hover:bg-orange-700 transition-colors"
                        >
                            Continue Shopping
                        </button>
                    </div>

                    <div v-else class="grid md:grid-cols-2 gap-6">
                        <div class="p-4 md:p-6 bg-green-50 rounded-md">
                            <h2
                                class="text-xl font-semibold text-green-600 mb-2"
                            >
                                Order Summary
                            </h2>
                            <ul
                                class="space-y-4 max-h-60 overflow-y-auto overscroll-contain"
                            >
                                <li
                                    v-for="item in cartStore.carts"
                                    :key="item.id"
                                    class="flex justify-between items-start gap-3"
                                >
                                    <div class="flex-1 min-w-0">
                                        <h3
                                            class="font-medium text-gray-700 truncate"
                                        >
                                            {{
                                                item.product?.name ||
                                                "Unknown Product"
                                            }}
                                        </h3>
                                        <p
                                            class="text-sm text-gray-500 truncate"
                                        >
                                            {{
                                                item.product?.description ||
                                                "No description"
                                            }}
                                        </p>
                                    </div>
                                    <div class="text-right flex-shrink-0">
                                        <p
                                            class="text-green-600 font-semibold whitespace-nowrap"
                                        >
                                            ₵{{ item.product?.price || 0 }} x
                                            {{ item.quantity || 0 }}
                                        </p>
                                        <p class="text-sm text-gray-600">
                                            ₵{{ cartStore.getItemTotal(item) }}
                                        </p>
                                    </div>
                                </li>
                            </ul>
                            <div class="border-t mt-4 pt-4">
                                <div
                                    class="flex justify-between gap-3 text-gray-600 font-medium"
                                >
                                    <span>Subtotal</span>
                                    <span>₵{{ cartStore.subtotal }}</span>
                                </div>
                                <div
                                    class="flex justify-between gap-3 text-gray-600 font-medium"
                                >
                                    <span>Delivery</span>
                                    <span>₵{{ delivery }}</span>
                                </div>
                                <div
                                    class="flex justify-between text-lg font-bold text-gray-600 mt-2"
                                >
                                    <span>Total</span>
                                    <span>₵{{ totalWithDelivery }}</span>
                                </div>
                            </div>
                        </div>

                        <div class="p-4 bg-white rounded">
                            <h2
                                class="text-xl font-semibold text-orange-600 mb-4"
                            >
                                Delivery Information
                            </h2>

                            <div
                                v-if="orderStore.error"
                                class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded"
                            >
                                {{ orderStore.error }}
                            </div>

                            <form
                                @submit.prevent="placeOrder"
                                class="space-y-4"
                            >
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
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
                                        class="mt-1 w-full border border-gray-400 rounded px-3 py-2 outline-none focus:border-orange-700 disabled:bg-gray-100 disabled:cursor-not-allowed"
                                        placeholder="Enter your full name"
                                    />
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
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
                                        class="mt-1 w-full border border-gray-400 rounded px-3 py-2 outline-none focus:border-orange-700 disabled:bg-gray-100 disabled:cursor-not-allowed"
                                        placeholder="Enter your phone number"
                                    />
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
                                    >
                                        Delivery Address *
                                    </label>
                                    <textarea
                                        v-model="form.address"
                                        required
                                        rows="3"
                                        :disabled="
                                            isLoading || orderStore.loading
                                        "
                                        class="mt-1 w-full border border-gray-400 rounded px-3 py-2 outline-none focus:border-orange-700 resize-none disabled:bg-gray-100 disabled:cursor-not-allowed"
                                        placeholder="Enter your delivery address"
                                    ></textarea>
                                </div>

                                <button
                                    type="submit"
                                    :disabled="
                                        isLoading ||
                                        orderStore.loading ||
                                        !isFormValid
                                    "
                                    class="w-full bg-orange-600 text-white py-3 px-4 rounded-lg hover:bg-orange-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
                                >
                                    <span
                                        v-if="isLoading || orderStore.loading"
                                    >
                                        <i
                                            class="pi pi-spin pi-spinner mr-2"
                                        ></i>
                                        Placing Order...
                                    </span>
                                    <span v-else>Confirm Order</span>
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
