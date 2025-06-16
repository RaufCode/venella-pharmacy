<script setup lang="ts">
    import { computed, onMounted } from "vue";
    import { useOrderStore } from "@/stores/orderStore";
    import { useAuthStore } from "@/stores/auth";
    import { useMedStore } from "@/stores/medStore";
    import { useNotificationStore } from "@/stores/notification"; // ✅ Import store

    import {
        ChartSpline,
        Bell,
        CircleDotDashed,
        ShoppingCart,
    } from "lucide-vue-next";

    const orderStore = useOrderStore();
    const authStore = useAuthStore();
    const medStore = useMedStore();
    const notificationStore = useNotificationStore(); // ✅ Store instance

    onMounted(() => {
        orderStore.fetchAllOrders();
        medStore.fetchProducts(); // Fetch meds to calculate stock
        notificationStore.startPolling(); // ✅ Optional: Start real-time updates
    });

    // ✅ Real notification count
    const notificationCount = computed(() => notificationStore.unreadCount);

    const totalSales = computed(() => {
        return orderStore.orders
            .filter((order) => order.status?.toLowerCase() === "delivered")
            .reduce((sum, order) => {
                const orderTotal =
                    order.order_items?.reduce((acc, item) => {
                        const amount = parseFloat(item.amount);
                        return acc + (isNaN(amount) ? 0 : amount);
                    }, 0) || 0;
                return sum + orderTotal;
            }, 0);
    });

    const totalDeliveredOrders = computed(() => {
        return orderStore.orders.filter(
            (order) => order.status?.toLowerCase() === "delivered"
        ).length;
    });

    const totalItemsDelivered = computed(() => {
        return orderStore.orders
            .filter((order) => order.status?.toLowerCase() === "delivered")
            .reduce((sum, order) => {
                const orderItemsCount =
                    order.order_items?.reduce((acc, item) => {
                        const quantity = parseInt(item.quantity) || 0;
                        return acc + quantity;
                    }, 0) || 0;
                return sum + orderItemsCount;
            }, 0);
    });

    const timeBasedGreeting = computed(() => {
        const hour = new Date().getHours();
        if (hour >= 5 && hour < 12) {
            return "Good morning";
        } else if (hour >= 12 && hour < 17) {
            return "Good afternoon";
        } else if (hour >= 17 && hour < 21) {
            return "Good evening";
        } else {
            return "Good night";
        }
    });

    // Total stock logic
    const totalStock = computed(() => {
        return medStore.products.reduce((sum, product) => {
            return sum + (product.stock || 0);
        }, 0);
    });

    const stockLevel = computed(() => {
        return totalStock.value < 100 ? "low" : "high";
    });
</script>

<template>
    <div class="h-screen w-full relative flex flex-col flex-1 overflow-hidden">
        <!-- Desktop Welcome Header -->
        <div
            class="hidden md:block w-full md:absolute shadow top-0 z-50 p-3 bg-gray-50"
        >
            <h1 class="text-gray-600 font-styleScript text-3xl">
                {{ timeBasedGreeting }}
                <span class="text-gray-700 font-semibold font-styleScript">
                    {{ authStore.user.profile.first_name || "Salesperson" }}
                </span>
            </h1>
        </div>

        <!-- Main Dashboard Cards -->
        <div class="mx-auto container m-4 md:mt-[75px]">
            <div
                class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 p-3"
            >
                <!-- Total Sales -->
                <div
                    class="flex items-center justify-between rounded-lg shadow hover:shadow-md transition-shadow p-6 bg-white"
                >
                    <div>
                        <p class="text-gray-500 font-medium text-sm">
                            Total Sales
                        </p>
                        <p
                            class="text-2xl font-semibold font-poppins text-green-500"
                        >
                            &#8373;{{ totalSales.toFixed(2) }}
                        </p>
                    </div>
                    <ChartSpline class="text-green-500 w-6 h-6" />
                </div>

                <!-- Notifications (real-time count) -->
                <div
                    class="flex items-center justify-between rounded-lg shadow hover:shadow-md transition-shadow p-6 bg-white"
                >
                    <div>
                        <p class="text-gray-500 font-medium text-sm">
                            Notifications
                        </p>
                        <p
                            class="text-2xl font-semibold font-poppins text-red-500"
                        >
                            {{ notificationCount }}
                        </p>
                    </div>
                    <Bell class="text-red-500 w-6 h-6" />
                </div>

                <!-- Stock Level -->
                <div
                    class="flex items-center justify-between rounded-lg shadow hover:shadow-md transition-shadow p-6 bg-white"
                >
                    <div>
                        <p class="text-gray-500 font-medium text-sm">
                            Stock level
                        </p>
                        <p
                            class="text-2xl font-semibold font-poppins text-blue-500"
                        >
                            {{ stockLevel }}
                        </p>
                    </div>
                    <CircleDotDashed class="text-blue-500 w-6 h-6" />
                </div>

                <!-- Total Delivered Orders -->
                <div
                    class="flex items-center justify-between rounded-lg shadow hover:shadow-md transition-shadow p-6 bg-white"
                >
                    <div>
                        <p class="text-gray-500 font-medium text-sm">
                            Total Orders
                        </p>
                        <p
                            class="text-2xl font-semibold font-poppins text-yellow-500"
                        >
                            {{ totalItemsDelivered }}
                        </p>
                    </div>
                    <ShoppingCart class="text-yellow-500 w-6 h-6" />
                </div>
            </div>
        </div>
    </div>
</template>
