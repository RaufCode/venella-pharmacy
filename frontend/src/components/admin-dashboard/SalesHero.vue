<template>
    <div class="p-4 space-y-6">
        <!-- Page Header -->
        <div class="flex flex-col md:flex-row md:items-center justify-between">
            <h2 class="text-2xl font-bold">Sales Overview</h2>
            <input
                type="date"
                v-model="selectedDate"
                class="mt-2 md:mt-0 border p-2 rounded"
            />
        </div>

        <!-- Sales Summary -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-white p-4 shadow rounded">
                <h3 class="text-gray-600 text-sm">Total Sales</h3>
                <p class="text-xl font-semibold">₵{{ totalSales }}</p>
            </div>
            <div class="bg-white p-4 shadow rounded">
                <h3 class="text-gray-600 text-sm">Orders</h3>
                <p class="text-xl font-semibold">{{ totalOrders }}</p>
            </div>
            <div class="bg-white p-4 shadow rounded">
                <h3 class="text-gray-600 text-sm">Top Product</h3>
                <p class="text-xl font-semibold">{{ topProduct }}</p>
            </div>
            <div class="bg-white p-4 shadow rounded">
                <h3 class="text-gray-600 text-sm">Average Order Value</h3>
                <p class="text-xl font-semibold">₵{{ averageOrderValue }}</p>
            </div>
        </div>

        <!-- Sales Chart Placeholder -->
        <div class="bg-white p-4 shadow rounded">
            <h3 class="text-lg font-semibold mb-2">Sales Trends</h3>
            <!-- Chart component (optional using Chart.js) -->
            <div
                class="h-64 bg-gray-100 flex items-center justify-center text-gray-500"
            >
                Chart goes here
            </div>
        </div>

        <!-- Recent Sales Table -->
        <div class="bg-white p-4 shadow rounded overflow-x-auto">
            <h3 class="text-lg font-semibold mb-2">Recent Sales</h3>
            <table class="min-w-full text-sm text-left">
                <thead class="bg-gray-100">
                    <tr>
                        <th class="p-2">Order ID</th>
                        <th class="p-2">Customer</th>
                        <th class="p-2">Product</th>
                        <th class="p-2">Date</th>
                        <th class="p-2">Amount</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="sale in filteredSales"
                        :key="sale.id"
                        class="border-t"
                    >
                        <td class="p-2">{{ sale.id }}</td>
                        <td class="p-2">{{ sale.customer }}</td>
                        <td class="p-2">{{ sale.product }}</td>
                        <td class="p-2">{{ sale.date }}</td>
                        <td class="p-2">₵{{ sale.amount }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed } from "vue";

    const selectedDate = ref("");
    const sales = ref([
        {
            id: 1,
            customer: "Kwame A.",
            product: "Paracetamol",
            date: "2025-05-04",
            amount: 20,
        },
        {
            id: 2,
            customer: "Ama S.",
            product: "Amoxicillin",
            date: "2025-05-03",
            amount: 35,
        },
        {
            id: 3,
            customer: "Kojo M.",
            product: "Ibuprofen",
            date: "2025-05-03",
            amount: 18,
        },
    ]);

    const totalSales = computed(() =>
        sales.value.reduce((sum, s) => sum + s.amount, 0)
    );
    const totalOrders = computed(() => sales.value.length);
    const averageOrderValue = computed(() =>
        sales.value.length
            ? (totalSales.value / sales.value.length).toFixed(2)
            : 0
    );
    const topProduct = computed(() => {
        const counts = {};
        sales.value.forEach((s) => {
            counts[s.product] = (counts[s.product] || 0) + 1;
        });
        return (
            Object.entries(counts).sort((a, b) => b[1] - a[1])[0]?.[0] || "-"
        );
    });

    const filteredSales = computed(() =>
        selectedDate.value
            ? sales.value.filter((s) => s.date === selectedDate.value)
            : sales.value
    );
</script>

<style scoped>
    /* Responsive tweaks can go here */
</style>
