<script setup>
    import { ref, onMounted, watch, computed } from "vue";
    import { useOrderStore } from "@/stores/orderStore";
    import { storeToRefs } from "pinia";
    import { useRouter } from "vue-router";

    const router = useRouter();

    const orderStore = useOrderStore();
    const { orders, loading, error } = storeToRefs(orderStore);

    const activeTab = ref("all");
    const currentPage = ref(1);
    const itemsPerPage = 7;

    const selectedDate = ref(null);
    const filterMode = ref("all");

    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();

    const getLocalDateString = (dateStr) => {
        const date = new Date(dateStr);
        return new Date(date.getFullYear(), date.getMonth(), date.getDate())
            .toISOString()
            .split("T")[0];
    };

    const today = getLocalDateString(new Date());

    const fetchOrdersByTab = async (tab) => {
        selectedDate.value = null;
        filterMode.value = "all";
        if (tab === "pending") {
            await orderStore.fetchPendingOrders();
        } else if (tab === "processing") {
            await orderStore.fetchProcessingOrders();
        } else {
            await orderStore.fetchAllOrders();
        }
    };

    onMounted(() => fetchOrdersByTab(activeTab.value));

    watch(activeTab, async (newTab) => {
        currentPage.value = 1;
        if (["all", "pending", "processing"].includes(newTab)) {
            await fetchOrdersByTab(newTab);
        }
    });

    const filteredOrders = computed(() => {
        if (filterMode.value === "today") {
            return orders.value.filter((order) => {
                return getLocalDateString(order.created_at) === today;
            });
        }

        if (filterMode.value === "thisMonth") {
            return orders.value.filter((order) => {
                const date = new Date(order.created_at);
                return (
                    date.getMonth() === currentMonth &&
                    date.getFullYear() === currentYear
                );
            });
        }

        if (filterMode.value === "exactDate" && selectedDate.value) {
            return orders.value.filter((order) => {
                return (
                    getLocalDateString(order.created_at) === selectedDate.value
                );
            });
        }

        return orders.value;
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

    const filterToday = async () => {
        activeTab.value = "today";
        filterMode.value = "today";
        await orderStore.fetchAllOrders();
    };

    const filterThisMonth = async () => {
        activeTab.value = "thisMonth";
        filterMode.value = "thisMonth";
        await orderStore.fetchAllOrders();
    };

    const filterByDate = async (e) => {
        activeTab.value = "exactDate";
        selectedDate.value = e.target.value;
        filterMode.value = "exactDate";
        await orderStore.fetchAllOrders();
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
</script>

<template>
    <div class="h-screen w-full flex flex-col">
        <header
            class="bg-white px-6 py-4 shadow w-full hidden md:block font-semibold"
        >
            <h1 class="text-3xl font-medium text-gray-600 font-styleScript">
                Orders Hub
            </h1>
        </header>

        <nav class="p-4 overflow-x-auto mb-4">
            <div class="flex gap-3 flex-nowrap w-full">
                <button
                    @click="setTab('all')"
                    :class="[
                        'px-4 py-2 rounded-full font-medium text-sm transition whitespace-nowrap',
                        activeTab === 'all'
                            ? 'bg-orange-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
                    ]"
                >
                    All Orders
                </button>

                <button
                    @click="setTab('pending')"
                    :class="[
                        'px-4 py-2 rounded-full font-medium text-sm transition whitespace-nowrap',
                        activeTab === 'pending'
                            ? 'bg-yellow-500 text-white'
                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200',
                    ]"
                >
                    Pending
                </button>

                <button
                    @click="setTab('processing')"
                    :class="[
                        'px-4 py-2 rounded-full font-medium text-sm transition whitespace-nowrap',
                        activeTab === 'processing'
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
                    ]"
                >
                    Processing
                </button>

                <button
                    @click="filterToday"
                    :class="[
                        'px-4 py-2 rounded-full font-medium text-sm transition whitespace-nowrap',
                        activeTab === 'today'
                            ? 'bg-green-500 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
                    ]"
                >
                    Today
                </button>

                <button
                    @click="filterThisMonth"
                    :class="[
                        'px-4 py-2 rounded-full font-medium text-sm transition whitespace-nowrap',
                        activeTab === 'thisMonth'
                            ? 'bg-emerald-700 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
                    ]"
                >
                    This Month
                </button>

                <input
                    type="date"
                    @change="filterByDate"
                    :class="[
                        'px-3 py-2 rounded-full text-sm outline-none whitespace-nowrap transition',
                        activeTab === 'exactDate'
                            ? 'bg-teal-500 text-white'
                            : 'bg-gray-100 text-gray-700 border-gray-300 hover:border-gray-400',
                    ]"
                />
            </div>
        </nav>

        <main class="flex-1 overflow-y-auto px-4 pb-4 h-full">
            <div v-if="loading" class="text-center py-10 text-gray-600">
                Loading orders...
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

            <div
                v-else
                class="p-0 lg:p-4 lg:shadow lg:bg-gray-50 lg:rounded-lg lg:h-full overflow-y-auto"
            >
                <div class="overflow-x-auto rounded-lg border bg-white">
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
                                class="hover:bg-gray-50 transition cursor-pointer"
                                @click="goToOrderDetails(order.id)"
                            >
                                <td class="px-4 py-3">
                                    {{ order.order_items.length }} item{{
                                        order.order_items.length > 1 ? "s" : ""
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
                        class="px-4 py-2 rounded-md border border-gray-300 hover:bg-gray-100 disabled:opacity-50"
                    >
                        <i class="pi pi-angle-double-left"></i>
                    </button>
                    <span>{{ currentPage }} of {{ totalPages }}</span>
                    <button
                        @click="goNext"
                        :disabled="!canGoNext"
                        class="px-4 py-2 rounded-md border border-gray-300 hover:bg-gray-100 disabled:opacity-50"
                    >
                        <i class="pi pi-angle-double-right"></i>
                    </button>
                </div>
            </div>
        </main>
    </div>
</template>

<style scoped>
    /* Add custom styles if needed */
</style>
