<script>
    import { ref } from "vue";

    const totalSales = ref(1000);
    const totalOrders = ref(150);
    const totalCustomers = ref(200);
    const totalMedications = ref(50);
</script>
<template>
    <main class="w-full p-4 md:w-3/4 lg:max-2xl:w-4/5">
        <h2 class="text-2xl font-bold mb-4">Welcome to the Admin Dashboard</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <div class="bg-white p-4 rounded shadow">
                <h3 class="text-lg font-semibold">Total Sales</h3>
                <p class="text-2xl">{{ totalSales }}</p>
            </div>
            <div class="bg-white p-4 rounded shadow">
                <h3 class="text-lg font-semibold">Total Orders</h3>
                <p class="text-2xl">{{ totalOrders }}</p>
            </div>
            <div class="bg-white p-4 rounded shadow">
                <h3 class="text-lg font-semibold">Total Customers</h3>
                <p class="text-2xl">{{ totalCustomers }}</p>
            </div>
            <div class="bg-white p-4 rounded shadow">
                <h3 class="text-lg font-semibold">Total Medications</h3>
                <p class="text-2xl">{{ totalMedications }}</p>
            </div>
        </div>
        <div class="bg-white p-4 rounded shadow mb-8">
            <h3 class="text-lg font-semibold mb-4">Recent Orders</h3>
            <!-- Add a table or list of recent orders here -->
        </div>
        <div class="bg-white p-4 rounded shadow">
            <h3 class="text-lg font-semibold mb-4">Notifications</h3>
            <!-- Add notifications or alerts here -->
        </div>
    </main>
</template>
