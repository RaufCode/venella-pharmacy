<script setup>
    import { onMounted, ref, computed } from "vue";
    import { useRouter } from "vue-router";
    import { useOrderStore } from "@/stores/orderStore";
    import { storeToRefs } from "pinia";
    import Spinner from "../ui/Spinner.vue";

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

    function getStatusClasses(status) {
        switch (status?.toLowerCase()) {
            case "pending":
                return "bg-yellow-100 text-yellow-800";
            case "delivered":
                return "bg-green-100 text-green-800";
            case "processing":
                return "bg-blue-100 text-blue-800";
            case "cancelled":
                return "bg-red-100 text-red-800";
            default:
                return "bg-gray-100 text-gray-800";
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

    // 🟧 Sort orders: Pending → Processing → Delivered → Others
    const sortedOrders = computed(() => {
        const priority = { pending: 1, processing: 2, delivered: 3 };
        return [...customerOrders.value].sort((a, b) => {
            const aStatus = a.status?.toLowerCase();
            const bStatus = b.status?.toLowerCase();
            return (priority[aStatus] || 99) - (priority[bStatus] || 99);
        });
    });
</script>

<template>
    <div
        class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-orange-50"
    >
        <!-- Header -->
        <div
            class="sticky top-0 z-10 bg-white/80 backdrop-blur-sm border-b border-gray-200 shadow-sm"
        >
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex items-center justify-between h-16">
                    <div class="flex items-center gap-3">
                        <div
                            class="w-10 h-10 bg-gradient-to-br from-orange-500 to-red-600 rounded-xl flex items-center justify-center"
                        >
                            <svg
                                class="w-6 h-6 text-white"
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
                        </div>
                        <div>
                            <h1
                                class="text-xl font-styleScript bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent"
                            >
                                My Orders
                            </h1>
                        </div>
                    </div>
                    <button
                        @click="goBack"
                        class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-gray-400 transition-all duration-200 shadow-sm"
                    >
                        <svg
                            class="w-4 h-4"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M15 19l-7-7 7-7"
                            ></path>
                        </svg>
                        Back
                    </button>
                </div>
            </div>
        </div>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Loading State -->
            <div v-if="loading" class="text-center py-16">
                <div
                    class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-orange-100 to-red-100 rounded-full mb-4"
                >
                    <div
                        class="w-8 h-8 border-4 border-orange-200 border-t-orange-600 rounded-full animate-spin"
                    ></div>
                </div>
                <p class="text-gray-600 font-medium">Loading your orders...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="max-w-md mx-auto">
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
                        Unable to load orders
                    </h3>
                    <p class="text-red-600 mb-4">{{ error }}</p>
                    <button
                        @click="orderStore.fetchCustomerOrders()"
                        class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
                    >
                        Try Again
                    </button>
                </div>
            </div>

            <!-- Empty State -->
            <div
                v-else-if="customerOrders.length === 0"
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
                                d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                            ></path>
                        </svg>
                    </div>
                    <h3 class="text-2xl font-bold text-gray-800 mb-4">
                        No orders yet
                    </h3>
                    <p class="text-gray-600 mb-8">
                        You haven't placed any orders. Start shopping to see
                        your orders here!
                    </p>
                    <button
                        @click="router.push('/')"
                        class="inline-flex items-center gap-2 bg-gradient-to-r from-orange-600 to-red-600 text-white px-8 py-3 rounded-xl hover:from-orange-700 hover:to-red-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 font-medium"
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
                                d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
                            ></path>
                        </svg>
                        Start Shopping
                    </button>
                </div>
            </div>

            <!-- Orders Grid -->
            <div v-else>
                <!-- Order Stats -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                    <!-- Total Orders -->
                    <div
                        class="bg-white rounded-xl p-4 shadow border border-gray-100"
                    >
                        <div class="flex items-center justify-between gap-3">
                            <div
                                class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center"
                            >
                                <svg
                                    class="w-5 h-5 text-blue-600"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                                    />
                                </svg>
                            </div>
                            <div class="text-right">
                                <p class="text-lg font-bold text-gray-800">
                                    {{ customerOrders.length }}
                                </p>
                                <p class="text-sm text-gray-600 font-semibold">
                                    Total
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Pending Orders -->
                    <div
                        class="bg-white rounded-xl p-4 shadow border border-gray-100"
                    >
                        <div class="flex items-center justify-between gap-3">
                            <div
                                class="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center"
                            >
                                <svg
                                    class="w-5 h-5 text-yellow-600"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                                    />
                                </svg>
                            </div>
                            <div class="text-right">
                                <p class="text-lg font-bold text-gray-800">
                                    {{
                                        customerOrders.filter(
                                            (o) =>
                                                o.status?.toLowerCase() ===
                                                "pending"
                                        ).length
                                    }}
                                </p>
                                <p class="text-sm text-gray-600 font-semibold">
                                    Pending
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Processing Orders -->
                    <div
                        class="bg-white rounded-xl p-4 shadow border border-gray-100"
                    >
                        <div class="flex items-center justify-between gap-3">
                            <div
                                class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center"
                            >
                                <svg
                                    class="w-5 h-5 text-blue-600"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                                    />
                                </svg>
                            </div>
                            <div class="text-right">
                                <p class="text-lg font-bold text-gray-800">
                                    {{
                                        customerOrders.filter(
                                            (o) =>
                                                o.status?.toLowerCase() ===
                                                "processing"
                                        ).length
                                    }}
                                </p>
                                <p class="text-sm text-gray-600 font-semibold">
                                    Processing
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Delivered Orders -->
                    <div
                        class="bg-white rounded-xl p-4 shadow border border-gray-100"
                    >
                        <div class="flex items-center justify-between gap-3">
                            <div
                                class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center"
                            >
                                <svg
                                    class="w-5 h-5 text-green-600"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M5 13l4 4L19 7"
                                    />
                                </svg>
                            </div>
                            <div class="text-right">
                                <p class="text-lg font-bold text-gray-800">
                                    {{
                                        customerOrders.filter(
                                            (o) =>
                                                o.status?.toLowerCase() ===
                                                "delivered"
                                        ).length
                                    }}
                                </p>
                                <p class="text-sm text-gray-600 font-semibold">
                                    Delivered
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Orders List -->
                <div
                    class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
                >
                    <div
                        v-for="order in sortedOrders"
                        :key="order.id"
                        @click="goToOrderDetails(order.id)"
                        class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl hover:border-gray-200 transition-all duration-200 cursor-pointer transform hover:scale-[1.02]"
                    >
                        <!-- Header -->
                        <div class="p-4 border-b border-gray-100">
                            <div class="flex items-start justify-between gap-3">
                                <div class="flex-1 min-w-0">
                                    <h3
                                        class="font-semibold text-gray-800 line-clamp-1"
                                    >
                                        {{
                                            order.order_items?.[0]?.product
                                                ?.name || "Order Items"
                                        }}
                                    </h3>
                                    <p
                                        v-if="order.order_items?.length > 1"
                                        class="text-sm text-gray-500 mt-1"
                                    >
                                        +{{ order.order_items.length - 1 }} more
                                        item{{
                                            order.order_items.length > 2
                                                ? "s"
                                                : ""
                                        }}
                                    </p>
                                </div>
                                <div class="flex-shrink-0">
                                    <span
                                        :class="getStatusClasses(order.status)"
                                        class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                                    >
                                        {{ order.status }}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- Content -->
                        <div class="p-4">
                            <div class="space-y-3">
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-600"
                                        >Order Total</span
                                    >
                                    <span
                                        class="font-bold text-lg text-green-600"
                                        >₵{{ order.total_amount }}</span
                                    >
                                </div>

                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-600"
                                        >Order Date</span
                                    >
                                    <span
                                        class="text-sm font-medium text-gray-800"
                                        >{{
                                            formatDate(order.created_at)
                                        }}</span
                                    >
                                </div>

                                <div
                                    v-if="order.order_items?.length"
                                    class="pt-2 border-t border-gray-100"
                                >
                                    <p class="text-xs text-gray-500 mb-2">
                                        Items ({{ order.order_items.length }})
                                    </p>
                                    <div class="space-y-1">
                                        <div
                                            v-for="item in order.order_items.slice(
                                                0,
                                                2
                                            )"
                                            :key="item.id"
                                            class="text-xs text-gray-600"
                                        >
                                            {{ item.product?.name }} ({{
                                                item.quantity
                                            }}x)
                                        </div>
                                        <div
                                            v-if="order.order_items.length > 2"
                                            class="text-xs text-gray-500"
                                        >
                                            ... and
                                            {{ order.order_items.length - 2 }}
                                            more
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Actions -->
                            <div class="mt-4 pt-3 border-t border-gray-100">
                                <div
                                    class="flex items-center justify-between gap-2"
                                >
                                    <button
                                        class="text-xs text-blue-600 hover:text-blue-700 font-medium"
                                    >
                                        View Details
                                    </button>
                                    <button
                                        v-if="
                                            ['pending', 'processing'].includes(
                                                order.status?.toLowerCase()
                                            )
                                        "
                                        @click.stop="deleteOrder(order.id)"
                                        class="text-xs text-red-600 hover:text-red-700 font-medium"
                                    >
                                        Cancel Order
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
