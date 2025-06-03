<script setup>
    import { onMounted } from "vue";
    import { useRouter } from "vue-router";
    import { useOrderStore } from "@/stores/orderStore";
    import { storeToRefs } from "pinia";

    const orderStore = useOrderStore();
    const { customerOrders, loading, error } = storeToRefs(orderStore);

    const router = useRouter();

    function goBack() {
        router.back();
    }

    function formatDate(dateStr) {
        const options = { year: "numeric", month: "short", day: "numeric" };
        return new Date(dateStr).toLocaleDateString(undefined, options);
    }

    function statusBadge(status) {
        const base = "px-3 py-1 rounded-full text-xs font-medium";
        switch (status?.toLowerCase()) {
            case "pending":
                return `${base} bg-yellow-100 text-yellow-700`;
            case "completed":
                return `${base} bg-green-100 text-green-700`;
            case "cancelled":
                return `${base} bg-red-100 text-red-700`;
            default:
                return `${base} bg-gray-100 text-gray-600`;
        }
    }

    async function deleteOrder(orderId) {
        const confirmed = confirm(
            "Are you sure you want to cancel/delete this order?"
        );
        if (!confirmed) return;

        try {
            await orderStore.deleteOrder(orderId);
            await orderStore.fetchCustomerOrders();
        } catch (err) {
            alert("Failed to delete the order.");
            console.error(err);
        }
    }

    onMounted(() => {
        orderStore.fetchCustomerOrders();
    });
</script>
<template>
    <div class="relative min-h-screen bg-gray-100 pt-20">
        <!-- Header Bar -->
        <div
            class="flex items-center gap-4 w-full md:absolute top-0 z-50 p-3 bg-gray-900"
        >
            <button
                @click="goBack"
                class="flex items-center text-gray-300 hover:text-orange-600 transition"
            >
                <i class="pi pi-arrow-left"></i>
            </button>
            <h1
                class="text-gray-300 font-styleScript text-center text-lg md:text-2xl"
            >
                Order History
            </h1>
        </div>

        <!-- Content -->
        <div class="max-w-5xl mx-auto px-4 py-8">
            <div v-if="loading" class="text-center py-10 text-gray-600">
                Loading your orders...
            </div>

            <div v-else-if="error" class="text-center text-red-500 py-10">
                {{ error }}
            </div>

            <div
                v-else-if="customerOrders.length === 0"
                class="text-center py-10 text-gray-600"
            >
                No orders found.
            </div>

            <!-- Order Cards -->
            <div class="grid md:grid-cols-2 gap-6" v-else>
                <div
                    v-for="order in customerOrders"
                    :key="order.id"
                    class="bg-white rounded-xl shadow-sm p-5 hover:shadow-md transition"
                >
                    <!-- Top Section -->
                    <div class="flex justify-between items-start mb-3">
                        <div class="flex-1">
                            <p
                                class="text-sm font-semibold text-gray-800 truncate"
                            >
                                {{ order.order_items?.[0]?.product?.name }}
                                <span
                                    v-if="order.order_items?.length > 1"
                                    class="text-gray-500 text-xs"
                                >
                                    + {{ order.order_items.length - 1 }} more
                                </span>
                            </p>
                            <p
                                class="text-xs text-gray-500 italic mt-1 max-h-10 overflow-hidden"
                            >
                                {{
                                    order.order_items?.[0]?.product
                                        ?.description ||
                                    "No description available."
                                }}
                            </p>
                        </div>
                        <span :class="statusBadge(order.status)">
                            {{ order.status }}
                        </span>
                    </div>

                    <!-- Order Items -->
                    <ul class="text-sm text-gray-700 mb-4 space-y-1">
                        <li
                            v-for="item in order.order_items || []"
                            :key="item.id"
                            class="flex justify-between"
                        >
                            <span>{{ item.product.name }}</span>
                            <span class="text-gray-500"
                                >x{{ item.quantity }}</span
                            >
                        </li>
                    </ul>

                    <!-- Order Summary -->
                    <div class="flex justify-between text-sm text-gray-600">
                        <span>Total:</span>
                        <span class="font-semibold text-orange-600"
                            >GH₵ {{ order.total_amount }}</span
                        >
                    </div>

                    <div class="text-right mt-2 text-xs text-gray-400">
                        {{ formatDate(order.created_at) }}
                    </div>

                    <!-- Cancel Button -->
                    <div
                        v-if="order.status?.toLowerCase() === 'pending'"
                        class="mt-4 text-right"
                    >
                        <button
                            @click="deleteOrder(order.id)"
                            class="text-red-600 text-xs hover:underline"
                        >
                            Cancel Order
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .font-styleScript {
        font-family: "Satisfy", cursive;
    }
</style>
