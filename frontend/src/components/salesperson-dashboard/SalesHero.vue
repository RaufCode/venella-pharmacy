<script setup>
    import { onMounted, ref, computed, watch } from "vue";
    import { useOrderStore } from "@/stores/orderStore";

    const orderStore = useOrderStore();

    onMounted(() => {
        orderStore.fetchAllOrders();
    });

    const searchDate = ref("");

    watch(searchDate, (val) => {
        orderStore.setSearchDate(val);
    });

    const orders = computed(() => orderStore.orders);

    // Utility to count total items in an array of orders
    function countItems(ordersArray) {
        return ordersArray.reduce((total, order) => {
            return (
                total +
                (order.order_items?.reduce(
                    (sum, item) => sum + (Number(item.quantity) || 0),
                    0
                ) || 0)
            );
        }, 0);
    }

    // Orders grouped by status
    const pendingOrders = computed(() =>
        orders.value.filter(
            (order) => order.status?.toLowerCase() === "pending"
        )
    );
    const processingOrders = computed(() =>
        orders.value.filter(
            (order) => order.status?.toLowerCase() === "processing"
        )
    );
    const deliveredOrders = computed(() =>
        orders.value.filter(
            (order) => order.status?.toLowerCase() === "delivered"
        )
    );
    const cancelledOrders = computed(() =>
        orders.value.filter(
            (order) => order.status?.toLowerCase() === "cancelled"
        )
    );

    // Item counts by status
    const totalItemsOrdered = computed(() => countItems(orders.value));
    const pendingItems = computed(() => countItems(pendingOrders.value));
    const processingItems = computed(() => countItems(processingOrders.value));
    const deliveredItems = computed(() => countItems(deliveredOrders.value));
    const cancelledItems = computed(() => countItems(cancelledOrders.value));

    // ✅ Corrected total revenue using item.amount
    function sumOrderAmounts(orderArray) {
        return orderArray.reduce((total, order) => {
            const orderTotal =
                order.order_items?.reduce((sum, item) => {
                    const amount = parseFloat(item.amount);
                    return sum + (isNaN(amount) ? 0 : amount);
                }, 0) || 0;
            return total + orderTotal;
        }, 0);
    }

    const totalRevenue = computed(() => sumOrderAmounts(deliveredOrders.value));

    const monthlyRevenue = computed(() => {
        const now = new Date();
        return sumOrderAmounts(
            deliveredOrders.value.filter((order) => {
                const orderDate = new Date(
                    order.created_at || order.date || order.order_date
                );
                return (
                    orderDate.getMonth() === now.getMonth() &&
                    orderDate.getFullYear() === now.getFullYear()
                );
            })
        );
    });

    const dailyRevenue = computed(() => {
        const now = new Date();
        return sumOrderAmounts(
            deliveredOrders.value.filter((order) => {
                const orderDate = new Date(
                    order.created_at || order.date || order.order_date
                );
                return (
                    orderDate.getDate() === now.getDate() &&
                    orderDate.getMonth() === now.getMonth() &&
                    orderDate.getFullYear() === now.getFullYear()
                );
            })
        );
    });

    const currentDay = computed(() => {
        const now = new Date();
        return now.toLocaleDateString(undefined, {
            weekday: "long",
            month: "short",
            day: "numeric",
        });
    });

    const searchedRevenue = computed(() => orderStore.searchedRevenue);
</script>

<template>
    <div class="p-6 space-y-10">
        <h1 class="text-3xl font-bold text-gray-900">📊 Sales Overview</h1>

        <div class="bg-white p-6 rounded-2xl shadow-md">
            <h2 class="text-xl text-gray-700 mb-4">Revenue Summary</h2>
            <div
                class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-800"
            >
                <div
                    class="bg-orange-50 border-l-4 border-orange-400 p-4 rounded-xl"
                >
                    <h3 class="font-semibold text-gray-600 mb-1">
                        Total Revenue
                    </h3>
                    <p class="text-lg font-bold text-gray-900">
                        ₵{{ totalRevenue.toFixed(2) }}
                    </p>
                </div>
                <div
                    class="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-xl"
                >
                    <h3 class="font-semibold text-gray-600 mb-1">
                        Monthly Revenue
                    </h3>
                    <p class="text-lg font-bold text-gray-900">
                        ₵{{ monthlyRevenue.toFixed(2) }}
                    </p>
                </div>
                <div
                    class="bg-green-50 border-l-4 border-green-400 p-4 rounded-xl"
                >
                    <h3 class="font-semibold text-gray-600 mb-1">
                        Daily Revenue ({{ currentDay }})
                    </h3>
                    <p class="text-lg font-bold text-gray-900">
                        ₵{{ dailyRevenue.toFixed(2) }}
                    </p>
                </div>
            </div>
        </div>

        <div class="bg-white p-6 rounded-2xl shadow-md">
            <h2 class="text-xl text-gray-700 mb-4">Order Status Summary</h2>
            <div class="overflow-x-auto">
                <table
                    class="min-w-full border border-gray-200 text-sm text-gray-800"
                >
                    <thead class="bg-gray-100 font-medium">
                        <tr>
                            <th class="py-3 px-4 text-left">Status</th>
                            <th class="py-3 px-4 text-left">Item Count</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100">
                        <tr>
                            <td class="py-3 px-4 font-medium">
                                Total Items Ordered
                            </td>
                            <td class="py-3 px-4 font-semibold">
                                {{ totalItemsOrdered }}
                            </td>
                        </tr>
                        <tr>
                            <td class="py-3 px-4 font-medium">Pending</td>
                            <td class="py-3 px-4 font-bold">
                                {{ pendingItems }}
                            </td>
                        </tr>
                        <tr>
                            <td class="py-3 px-4 font-medium">Processing</td>
                            <td class="py-3 px-4 font-bold">
                                {{ processingItems }}
                            </td>
                        </tr>
                        <tr>
                            <td class="py-3 px-4 font-medium">Delivered</td>
                            <td class="py-3 px-4 font-bold">
                                {{ deliveredItems }}
                            </td>
                        </tr>
                        <tr>
                            <td class="py-3 px-4 font-medium">Cancelled</td>
                            <td class="py-3 px-4 font-bold">
                                {{ cancelledItems }}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>
