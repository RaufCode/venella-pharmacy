<script setup>
    import { ref, onMounted, watch, computed } from "vue";
    import { useOrderStore } from "@/stores/orderStore";
    import { storeToRefs } from "pinia";
    import { useRouter } from "vue-router";
    import Spinner from "../ui/Spinner.vue";

    const router = useRouter();

    const orderStore = useOrderStore();
    const { orders, loading, error } = storeToRefs(orderStore);

    const activeTab = ref("all");
    const currentPage = ref(1);
    const itemsPerPage = 7;

    const selectedDate = ref(null);

    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();

    // Fixed date comparison function
    const getLocalDateString = (dateStr) => {
        const date = new Date(dateStr);
        // Create date in local timezone to avoid UTC conversion issues
        const localDate = new Date(
            date.getTime() + date.getTimezoneOffset() * 60000
        );
        return localDate.toISOString().split("T")[0];
    };

    const today = new Date().toISOString().split("T")[0];

    const fetchOrdersByTab = async (tab) => {
        // Reset page when changing tabs
        currentPage.value = 1;

        if (tab === "pending") {
            await orderStore.fetchPendingOrders();
        } else if (tab === "processing") {
            await orderStore.fetchProcessingOrders();
        } else {
            // For all other tabs (all, today, thisMonth, exactDate), fetch all orders
            await orderStore.fetchAllOrders();
        }
    };

    onMounted(() => fetchOrdersByTab(activeTab.value));

    watch(activeTab, async (newTab) => {
        // Clear date selection when switching away from exactDate
        if (newTab !== "exactDate") {
            selectedDate.value = null;
        }
        await fetchOrdersByTab(newTab);
    });

    // Fixed filtering logic
    const filteredOrders = computed(() => {
        let filtered = [...orders.value];

        if (activeTab.value === "today") {
            filtered = filtered.filter((order) => {
                return getLocalDateString(order.created_at) === today;
            });
        } else if (activeTab.value === "thisMonth") {
            filtered = filtered.filter((order) => {
                const date = new Date(order.created_at);
                return (
                    date.getMonth() === currentMonth &&
                    date.getFullYear() === currentYear
                );
            });
        } else if (activeTab.value === "exactDate" && selectedDate.value) {
            filtered = filtered.filter((order) => {
                return (
                    getLocalDateString(order.created_at) === selectedDate.value
                );
            });
        }
        // For 'all', 'pending', 'processing' tabs, return all orders (already filtered by API)

        return filtered;
    });

    const paginatedOrders = computed(() => {
        const start = (currentPage.value - 1) * itemsPerPage;
        return filteredOrders.value.slice(start, start + itemsPerPage);
    });

    const totalPages = computed(() =>
        Math.ceil(filteredOrders.value.length / itemsPerPage)
    );

    const canGoPrev = computed(() => currentPage.value > 1);
    const canGoNext = computed(() => currentPage.value < totalPages.value);

    const goPrev = () => {
        if (canGoPrev.value) currentPage.value--;
    };

    const goNext = () => {
        if (canGoNext.value) currentPage.value++;
    };

    const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString();

    const setTab = (tab) => {
        activeTab.value = tab;
    };

    // Simplified filter functions
    const filterToday = () => {
        activeTab.value = "today";
    };

    const filterThisMonth = () => {
        activeTab.value = "thisMonth";
    };

    const filterByDate = (e) => {
        selectedDate.value = e.target.value;
        activeTab.value = "exactDate";
    };

    const updateStatusAndRefresh = async (orderId, newStatus) => {
        await orderStore.updateOrderStatus(orderId, newStatus);
        await fetchOrdersByTab(activeTab.value);
    };

    const markAsProcessing = (orderId) =>
        updateStatusAndRefresh(orderId, "processing");

    const markAsDelivered = (orderId) =>
        updateStatusAndRefresh(orderId, "delivered");

    const goToOrderDetails = (orderId) => {
        router.push(`order/${orderId}`);
    };

    // Reset to first page when filtered results change
    watch(filteredOrders, () => {
        if (currentPage.value > totalPages.value && totalPages.value > 0) {
            currentPage.value = 1;
        }
    });
</script>

<template>
    <div class="h-screen w-full flex flex-col">
        <header
            class="bg-gray-50 px-6 py-4 shadow w-full hidden md:block font-semibold fixed top-0 z-50"
        >
            <h1 class="text-3xl font-medium text-gray-600 font-styleScript">
                Orders Hub
            </h1>
        </header>
        <div class="container mx-auto mt-3 md:mt-16">
            <nav class="m-4 overflow-x-auto">
                <div class="flex gap-6 justify-between flex-nowrap w-full">
                    <button
                        @click="setTab('all')"
                        :class="[
                            'py-2 font-semibold text-sm border-b-2 transition-colors duration-200 ease-in-out whitespace-nowrap',
                            activeTab === 'all'
                                ? 'text-orange-600 border-orange-600'
                                : 'text-gray-500 border-transparent hover:text-orange-500',
                        ]"
                    >
                        All Orders
                    </button>

                    <button
                        @click="setTab('pending')"
                        :class="[
                            'py-2 font-semibold text-sm border-b-2 transition-colors duration-200 ease-in-out whitespace-nowrap',
                            activeTab === 'pending'
                                ? 'text-yellow-500 border-yellow-500'
                                : 'text-gray-500 border-transparent hover:text-yellow-400',
                        ]"
                    >
                        Pending
                    </button>

                    <button
                        @click="setTab('processing')"
                        :class="[
                            'py-2 font-semibold text-sm border-b-2 transition-colors duration-200 ease-in-out whitespace-nowrap',
                            activeTab === 'processing'
                                ? 'text-green-500 border-green-500'
                                : 'text-gray-500 border-transparent hover:text-green-400',
                        ]"
                    >
                        Processing
                    </button>

                    <button
                        @click="filterThisMonth"
                        :class="[
                            'py-2 font-semibold text-sm border-b-2 transition-colors duration-200 ease-in-out whitespace-nowrap',
                            activeTab === 'thisMonth'
                                ? 'text-emerald-500 border-emerald-500'
                                : 'text-gray-500 border-transparent hover:text-emerald-400',
                        ]"
                    >
                        This Month
                    </button>

                    <button
                        @click="filterToday"
                        :class="[
                            'py-2 font-semibold text-sm border-b-2 transition-colors duration-200 ease-in-out whitespace-nowrap',
                            activeTab === 'today'
                                ? 'text-blue-500 border-blue-500'
                                : 'text-gray-500 border-transparent hover:text-blue-400',
                        ]"
                    >
                        Today
                    </button>

                    <input
                        type="date"
                        @change="filterByDate"
                        v-model="selectedDate"
                        :class="[
                            'text-sm outline-none border-b-2 whitespace-nowrap transition',
                            activeTab === 'exactDate'
                                ? 'border-teal-500 text-teal-500'
                                : 'text-gray-500 border-transparent hover:text-teal-400',
                        ]"
                    />
                </div>
            </nav>

            <main class="flex-1 overflow-y-auto px-4 pb-4 h-full">
                <div v-if="loading" class="text-center py-10 text-gray-600">
                    <Spinner />
                </div>
                <div v-else-if="error" class="text-center py-10 text-red-600">
                    {{ error }}
                </div>
                <div
                    v-else-if="!filteredOrders.length"
                    class="text-center py-10 text-gray-500"
                >
                    No orders found for this filter.
                </div>

                <div v-else class="">
                    <div class="overflow-x-auto bg-white">
                        <table
                            class="min-w-full divide-y divide-gray-200 shadow text-sm"
                        >
                            <thead class="bg-gray-200 text-gray-600 text-left">
                                <tr>
                                    <th class="px-4 py-3">Items</th>
                                    <th class="px-4 py-3">Date</th>
                                    <th class="px-4 py-3">Status</th>
                                    <th class="px-4 py-3">Type</th>
                                    <th class="px-4 py-3 truncate">GH₵</th>
                                    <th class="px-4 py-3">Address</th>
                                    <th
                                        v-if="
                                            activeTab === 'pending' ||
                                            activeTab === 'processing'
                                        "
                                        class="px-4 py-3"
                                    >
                                        Action
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-100">
                                <tr
                                    v-for="order in paginatedOrders"
                                    :key="order.id"
                                    class="hover:bg-gray-50 transition cursor-pointer hover:shadow-lg"
                                    @click="goToOrderDetails(order.id)"
                                >
                                    <td class="px-4 py-3">
                                        {{ order.order_items.length }} item{{
                                            order.order_items.length > 1
                                                ? "s"
                                                : ""
                                        }}
                                    </td>
                                    <td class="px-4 py-3">
                                        {{ formatDate(order.created_at) }}
                                    </td>
                                    <td
                                        class="px-4 py-3 font-medium text-[12px]"
                                        :class="{
                                            'text-yellow-500':
                                                order.status === 'PENDING',
                                            'text-blue-500':
                                                order.status === 'PROCESSING',
                                            'text-green-500':
                                                order.status === 'DELIVERED',
                                            'text-red-500':
                                                order.status === 'CANCELLED',
                                        }"
                                    >
                                        {{ order.status }}
                                    </td>
                                    <td class="px-4 py-3 text-[12px]">
                                        {{ order.order_type }}
                                    </td>
                                    <td
                                        class="px-4 py-3 font-medium text-orange-600"
                                    >
                                        {{ order.total_amount }}
                                    </td>
                                    <td
                                        class="px-4 py-3 truncate max-w-[250px]"
                                        :title="order.shipping_address"
                                    >
                                        {{ order.shipping_address }}
                                    </td>
                                    <td
                                        v-if="activeTab === 'pending'"
                                        class="px-4 py-3"
                                        @click.stop
                                    >
                                        <button
                                            @click="markAsProcessing(order.id)"
                                            class="bg-yellow-500 text-white px-3 py-1 rounded-full hover:bg-yellow-600 transition"
                                        >
                                            Process
                                        </button>
                                    </td>
                                    <td
                                        v-else-if="activeTab === 'processing'"
                                        class="px-4 py-3"
                                        @click.stop
                                    >
                                        <button
                                            @click="markAsDelivered(order.id)"
                                            class="bg-blue-500 text-white px-3 py-1 rounded-full hover:bg-blue-600 transition"
                                        >
                                            Delivered
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div
                        v-if="totalPages > 1"
                        class="flex justify-center items-center gap-4 my-4"
                    >
                        <button
                            @click="goPrev"
                            :disabled="!canGoPrev"
                            class="px-4 py-2 rounded-md bg-white border border-gray-300 hover:bg-gray-100 disabled:opacity-50"
                        >
                            <i class="pi pi-angle-double-left"></i>
                        </button>
                        <span>{{ currentPage }} of {{ totalPages }}</span>
                        <button
                            @click="goNext"
                            :disabled="!canGoNext"
                            class="px-4 py-2 rounded-md bg-white border border-gray-300 hover:bg-gray-100 disabled:opacity-50"
                        >
                            <i class="pi pi-angle-double-right"></i>
                        </button>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<style scoped>
    /* Add custom styles if needed */
</style>
