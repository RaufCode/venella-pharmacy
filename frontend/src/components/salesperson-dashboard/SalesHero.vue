<script setup>
    import { onMounted, ref, computed, watch } from "vue";
    import { useOrderStore } from "@/stores/orderStore";

    const orderStore = useOrderStore();

    const searchDate = ref("");

    onMounted(() => {
        orderStore.fetchAllOrders();
    });

    watch(searchDate, (val) => {
        orderStore.setSearchDate(val);
    });

    const orders = computed(() => orderStore.orders);

    // Utility to count total items
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

    // Orders by status
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

    // Item counts
    const totalItemsOrdered = computed(() => countItems(orders.value));
    const pendingItems = computed(() => countItems(pendingOrders.value));
    const processingItems = computed(() => countItems(processingOrders.value));
    const deliveredItems = computed(() => countItems(deliveredOrders.value));
    const cancelledItems = computed(() => countItems(cancelledOrders.value));

    // Sum revenue using item.amount
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
                const dateStr =
                    order.created_at || order.date || order.order_date;
                if (!dateStr) return false;
                const orderDate = new Date(dateStr);
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
    <div class="">
        <div class="hidden md:block p-4 shadow font-semibold">
            <h1 class="text-3xl font-medium text-gray-600 font-styleScript">
                Sales Hub
            </h1>
        </div>

        <div
            class="p-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-sm text-gray-800"
        >
            <div class="p-8 shadow-md rounded-xl">
                <h3 class="font-semibold text-green-600">Total Revenue</h3>
                <p class="font-semibold text-gray-700 mt-2">
                    ₵{{ totalRevenue.toFixed(2) }}
                </p>
            </div>
            <div class="p-8 shadow-md rounded-xl">
                <h3 class="font-semibold text-yellow-500">Monthly Revenue</h3>
                <p class="font-semibold text-gray-700 mt-2">
                    ₵{{ monthlyRevenue.toFixed(2) }}
                </p>
            </div>
            <div class="p-8 shadow-md rounded-xl">
                <h3 class="font-semibold text-orange-500">
                    {{ currentDay }}
                </h3>
                <p class="font-semibold text-gray-700 mt-2">
                    ₵{{ dailyRevenue.toFixed(2) }}
                </p>
            </div>
        </div>

        <div class="overflow-x-auto p-4 pt-0">
            <h1
                class="md:text-base text-center pb-4 font-medium text-orange-600"
            >
                ORDER SUMMARY
            </h1>
            <div class="overflow-x-auto rounded-lg border bg-white">
                <table class="min-w-full text-sm text-gray-600 rounded-lg">
                    <thead class="bg-gray-100 font-medium">
                        <tr>
                            <th class="py-3 px-4 text-left">Status</th>
                            <th class="py-3 px-4 text-left">Number</th>
                        </tr>
                    </thead>
                    <tbody
                        class="divide-y divide-gray-100 text-gray-600 font-medium"
                    >
                        <tr>
                            <td class="py-3 px-4">Total Items Ordered</td>
                            <td class="py-3 px-4">
                                {{ totalItemsOrdered }}
                            </td>
                        </tr>
                        <tr>
                            <td class="py-3 px-4">Pending</td>
                            <td class="py-3 px-4">
                                {{ pendingItems }}
                            </td>
                        </tr>
                        <tr>
                            <td class="py-3 px-4">Processing</td>
                            <td class="py-3 px-4">
                                {{ processingItems }}
                            </td>
                        </tr>
                        <tr>
                            <td class="py-3 px-4">Delivered</td>
                            <td class="py-3 px-4">
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
