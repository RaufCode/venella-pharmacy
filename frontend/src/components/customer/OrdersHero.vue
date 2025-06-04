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
        const base = "rounded-full text-xs pt-2 font-medium";
        switch (status?.toLowerCase()) {
            case "pending":
                return `${base}  text-yellow-500`;
            case "delivered":
                return `${base} text-green-500`;
            case "processing":
                return `${base} text-blue-500`;
            case "cancelled":
                return `${base}  text-red-500`;
            default:
                return `${base} text-gray-600`;
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

    function goToOrderDetails(orderId) {
        router.push(`order/${orderId}`);
    }
</script>
<template>
    <div class="min-h-screen w-full">
        <!-- Header Bar -->
        <div
            class="flex items-center justify-between gap-4 w-full p-4 lg:px-10 fixed top-0 shadow-sm bg-white"
        >
            <h1
                class="text-gray-700 font-styleScript text-center text-lg md:text-2xl"
            >
                Order Hub
            </h1>
            <button
                @click="goBack"
                class="px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-full flex justify-center items-center gap-3"
            >
                <i class="pi pi-arrow-left"></i> Back
            </button>
        </div>
        <div class="container mx-auto">
            <!-- Content -->
            <div class="w-full">
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
                <div
                    class="grid grid-col-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mx-4 mt-24"
                    v-else
                >
                    <div
                        v-for="order in customerOrders"
                        :key="order.id"
                        @click="goToOrderDetails(order.id)"
                        class="bg-white rounded-xl shadow-sm p-5 hover:shadow-md transition cursor-pointer"
                    >
                        <!-- Top Section -->
                        <div class="mb-3">
                            <div class="">
                                <p
                                    class="text-sm font-semibold text-gray-800 truncate"
                                >
                                    {{ order.order_items?.[0]?.product?.name }}
                                    <span
                                        v-if="order.order_items?.length > 1"
                                        class="text-gray-500 text-xs"
                                    >
                                        +
                                        {{ order.order_items.length - 1 }} more
                                    </span>
                                </p>
                            </div>
                            <p :class="statusBadge(order.status)">
                                {{ order.status }}
                            </p>
                        </div>

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
                            v-if="
                                ['pending', 'processing'].includes(
                                    order.status?.toLowerCase()
                                )
                            "
                            class="mt-2 text-right"
                        >
                            <button
                                @click="deleteOrder(order.id)"
                                class="text-red-600 text-sm"
                            >
                                Cancel
                            </button>
                        </div>
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
