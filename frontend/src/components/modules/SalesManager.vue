<script setup>
    import { ref, computed, onMounted, watch } from "vue";
    import {
        TrendingUp,
        TrendingDown,
        DollarSign,
        ShoppingCart,
        Package,
        Users,
        BarChart3,
        ChevronLeft,
        ChevronRight,
    } from "lucide-vue-next";

    import BaseCard from "@/components/shared/BaseCard.vue";
    import BaseButton from "@/components/shared/BaseButton.vue";
    import BaseInput from "@/components/shared/BaseInput.vue";
    import Spinner from "@/components/ui/Spinner.vue";

    import { useOrderStore } from "@/stores/orderStore";

    const props = defineProps({
        userRole: {
            type: String,
            required: true,
        },
    });

    const orderStore = useOrderStore();

    const selectedDate = ref("");
    const selectedPeriod = ref("month");
    const currentPage = ref(1);
    const itemsPerPage = 10;

    const isLoading = computed(() => orderStore.loading);
    const orders = computed(() => orderStore.orders || []);

    // Filter orders based on selected period and date
    const filteredOrders = computed(() => {
        let filtered = orders.value.filter(
            (order) => order.status?.toLowerCase() === "delivered"
        );

        if (selectedDate.value) {
            filtered = filtered.filter((order) => {
                const orderDate = new Date(order.created_at)
                    .toISOString()
                    .split("T")[0];
                return orderDate === selectedDate.value;
            });
        } else {
            const now = new Date();
            const filterDate = new Date();

            switch (selectedPeriod.value) {
                case "today":
                    filterDate.setHours(0, 0, 0, 0);
                    filtered = filtered.filter(
                        (order) => new Date(order.created_at) >= filterDate
                    );
                    break;
                case "week":
                    filterDate.setDate(now.getDate() - 7);
                    filtered = filtered.filter(
                        (order) => new Date(order.created_at) >= filterDate
                    );
                    break;
                case "month":
                    filterDate.setMonth(now.getMonth() - 1);
                    filtered = filtered.filter(
                        (order) => new Date(order.created_at) >= filterDate
                    );
                    break;
                case "year":
                    filterDate.setFullYear(now.getFullYear() - 1);
                    filtered = filtered.filter(
                        (order) => new Date(order.created_at) >= filterDate
                    );
                    break;
            }
        }

        return filtered.sort(
            (a, b) => new Date(b.created_at) - new Date(a.created_at)
        );
    });

    const salesData = computed(() => filteredOrders.value);

    const salesMetrics = computed(() => {
        const totalRevenue = salesData.value.reduce(
            (sum, order) => sum + parseFloat(order.total_amount || 0),
            0
        );
        const totalOrders = salesData.value.length;
        const totalItems = salesData.value.reduce(
            (sum, order) => sum + (order.order_items?.length || 0),
            0
        );
        const avgOrderValue = totalOrders > 0 ? totalRevenue / totalOrders : 0;

        return [
            {
                label: "Total Revenue",
                value: `₵${totalRevenue.toFixed(2)}`,
                change: 12,
                changeType: "increase",
                icon: DollarSign,
                bgColor: "bg-green-100",
                iconColor: "text-green-600",
            },
            {
                label: "Orders",
                value: totalOrders,
                change: 8,
                changeType: "increase",
                icon: ShoppingCart,
                bgColor: "bg-blue-100",
                iconColor: "text-blue-600",
            },
            {
                label: "Items Sold",
                value: totalItems,
                change: 15,
                changeType: "increase",
                icon: Package,
                bgColor: "bg-purple-100",
                iconColor: "text-purple-600",
            },
            {
                label: "Avg Order Value",
                value: `₵${avgOrderValue.toFixed(2)}`,
                change: 5,
                changeType: "increase",
                icon: TrendingUp,
                bgColor: "bg-orange-100",
                iconColor: "text-orange-600",
            },
        ];
    });

    const topProducts = computed(() => {
        const productSales = {};

        salesData.value.forEach((order) => {
            order.order_items?.forEach((item) => {
                const productName = item.product?.name || "Unknown Product";

                if (!productSales[productName]) {
                    productSales[productName] = {
                        id: item.product?.id || Math.random(),
                        name: productName,
                        sales_count: 0,
                        total_revenue: 0,
                    };
                }
                productSales[productName].sales_count += parseInt(
                    item.quantity || 0
                );
                productSales[productName].total_revenue +=
                    parseFloat(item.price || 0) * parseInt(item.quantity || 0);
            });
        });

        return Object.values(productSales)
            .sort((a, b) => b.total_revenue - a.total_revenue)
            .slice(0, 5);
    });

    const totalPages = computed(() =>
        Math.ceil(salesData.value.length / itemsPerPage)
    );

    const paginatedSales = computed(() => {
        const start = (currentPage.value - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        return salesData.value.slice(start, end);
    });

    const getStatusClasses = (status) => {
        const baseClasses = "px-2 py-1 text-xs font-medium rounded-full";
        switch (status?.toLowerCase()) {
            case "delivered":
                return `${baseClasses} bg-green-100 text-green-800`;
            default:
                return `${baseClasses} bg-gray-100 text-gray-800`;
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString();
    };

    const formatTime = (dateString) => {
        return new Date(dateString).toLocaleTimeString();
    };

    const getTotalQuantity = (orderItems) => {
        return (
            orderItems?.reduce(
                (sum, item) => sum + parseInt(item.quantity || 0),
                0
            ) || 0
        );
    };

    watch(selectedPeriod, () => {
        currentPage.value = 1;
    });

    watch(selectedDate, () => {
        currentPage.value = 1;
    });

    onMounted(() => {
        orderStore.fetchAllOrders();
    });
</script>
<template>
    <div class="space-y-6">
        <Spinner v-if="isLoading" />
        <!-- Header -->
        <div
            class="flex flex-col lg:flex-row lg:items-center justify-between gap-4"
        >
            <div>
                <h2 class="text-xl text-gray-600">Sales Analytics</h2>
            </div>

            <div class="flex items-center gap-3">
                <BaseInput type="date" v-model="selectedDate" size="sm" />

                <select
                    v-model="selectedPeriod"
                    class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                >
                    <option value="today">Today</option>
                    <option value="week">This Week</option>
                    <option value="month">This Month</option>
                    <option value="year">This Year</option>
                </select>
            </div>
        </div>

        <!-- Sales Overview -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div
                v-for="metric in salesMetrics"
                :key="metric.label"
                class="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
            >
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm font-medium text-gray-600">
                            {{ metric.label }}
                        </p>
                        <p class="text-2xl font-semibold text-gray-900 mt-1">
                            {{ metric.value }}
                        </p>
                    </div>
                    <div
                        :class="[
                            'w-12 h-12 rounded-lg flex items-center justify-center',
                            metric.bgColor,
                        ]"
                    >
                        <component
                            :is="metric.icon"
                            :class="['w-6 h-6', metric.iconColor]"
                        />
                    </div>
                </div>
            </div>
        </div>

        <!-- Charts Section -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Top Products -->
            <BaseCard
                title="Top Selling Products"
                subtitle="Best performing medications"
            >
                <div class="space-y-4">
                    <div
                        v-for="(product, index) in topProducts"
                        :key="product.id"
                        class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg"
                    >
                        <div class="flex-shrink-0">
                            <div
                                class="w-8 h-8 bg-orange-100 text-orange-600 rounded-full flex items-center justify-center text-sm font-semibold"
                            >
                                {{ index + 1 }}
                            </div>
                        </div>
                        <div class="flex-1 min-w-0">
                            <p
                                class="text-sm font-medium text-gray-900 truncate"
                            >
                                {{ product.name }}
                            </p>
                            <p class="text-xs text-gray-500">
                                {{ product.sales_count }} units sold
                            </p>
                        </div>
                    </div>

                    <div
                        v-if="topProducts.length === 0"
                        class="text-center py-8"
                    >
                        <Package class="w-8 h-8 text-gray-300 mx-auto mb-2" />
                        <p class="text-sm text-gray-500">
                            No sales data available
                        </p>
                    </div>
                </div>
            </BaseCard>
        </div>

        <!-- Detailed Sales Table -->
        <BaseCard title="Recent Sales" subtitle="Detailed sales transactions">
            <div
                v-if="isLoading"
                class="flex items-center justify-center py-12"
            >
                <div
                    class="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"
                ></div>
            </div>

            <div v-else-if="salesData.length === 0" class="text-center py-12">
                <TrendingUp class="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <h3 class="text-lg font-medium text-gray-900">No sales data</h3>
                <p class="text-gray-500">
                    Sales transactions will appear here.
                </p>
            </div>

            <div v-else>
                <!-- Desktop Table -->
                <div class="hidden md:block overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Order ID
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Customer Email
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Items
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Date
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Amount
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Status
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr
                                v-for="sale in paginatedSales"
                                :key="sale.id"
                                class="hover:bg-gray-50 transition-colors"
                            >
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div
                                        class="text-sm font-medium text-gray-900"
                                    >
                                        #{{ sale.id }}
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div
                                        class="text-sm font-medium text-gray-900"
                                    >
                                        {{ sale.customer.email }}
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="text-sm text-gray-900">
                                        {{ sale.order_items?.length || 0 }}
                                        items
                                    </div>
                                    <div class="text-sm text-gray-500">
                                        {{ getTotalQuantity(sale.order_items) }}
                                        units
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="text-sm text-gray-900">
                                        {{ formatDate(sale.created_at) }}
                                    </div>
                                    <div class="text-sm text-gray-500">
                                        {{ formatTime(sale.created_at) }}
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div
                                        class="text-sm font-semibold text-gray-900"
                                    >
                                        ₵{{
                                            parseFloat(
                                                sale.total_amount || 0
                                            ).toFixed(2)
                                        }}
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span
                                        :class="getStatusClasses(sale.status)"
                                    >
                                        {{ sale.status }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Mobile Cards -->
                <div class="md:hidden space-y-4">
                    <div
                        v-for="sale in paginatedSales"
                        :key="sale.id"
                        class="bg-white border border-gray-200 rounded-lg p-4 shadow-sm"
                    >
                        <div class="flex items-start justify-between mb-3">
                            <div>
                                <h3 class="text-sm font-medium text-gray-900">
                                    #{{ sale.id }}
                                </h3>
                                <p class="text-xs text-gray-500 mt-1">
                                    {{ sale.customer_name }}
                                </p>
                            </div>
                            <span :class="getStatusClasses(sale.status)">
                                {{ sale.status }}
                            </span>
                        </div>

                        <div class="space-y-2 text-sm">
                            <div class="flex items-center justify-between">
                                <span class="text-gray-600">Items:</span>
                                <span
                                    >{{ sale.order_items?.length || 0 }} ({{
                                        getTotalQuantity(sale.order_items)
                                    }}
                                    units)</span
                                >
                            </div>
                            <div class="flex items-center justify-between">
                                <span class="text-gray-600">Date:</span>
                                <span>{{ formatDate(sale.created_at) }}</span>
                            </div>
                            <div class="flex items-center justify-between">
                                <span class="text-gray-600">Amount:</span>
                                <span class="font-semibold"
                                    >₵{{
                                        parseFloat(
                                            sale.total_amount || 0
                                        ).toFixed(2)
                                    }}</span
                                >
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Pagination -->
                <div v-if="totalPages > 1" class="mx-auto w-max mt-6">
                    <div class="flex items-center gap-2">
                        <BaseButton
                            variant="outline"
                            size="sm"
                            :disabled="currentPage === 1"
                            @click="currentPage--"
                        >
                            <ChevronLeft class="w-4 h-4" />
                        </BaseButton>

                        <span
                            class="px-3 py-1 text-sm bg-orange-100 text-orange-700 rounded-lg"
                        >
                            {{ currentPage }} of {{ totalPages }}
                        </span>

                        <BaseButton
                            variant="outline"
                            size="sm"
                            :disabled="currentPage === totalPages"
                            @click="currentPage++"
                        >
                            <ChevronRight class="w-4 h-4" />
                        </BaseButton>
                    </div>
                </div>
            </div>
        </BaseCard>
    </div>
</template>
