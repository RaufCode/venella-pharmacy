<script setup>
    import { onMounted } from "vue";
    import { useRouter } from "vue-router";
    import { useOrderStore } from "@/stores/orderStore";
    import { useAuthStore } from "@/stores/auth";

    // Grab 'id' from route props
    const props = defineProps({
        id: String,
    });

    const router = useRouter();
    const orderStore = useOrderStore();
    const authStore = useAuthStore();

    const orderId = props.id; // 👈 use the prop, not route.params

    onMounted(async () => {
        await orderStore.fetchOrderDetails(orderId);
    });

    const goBack = () => {
        router.push({ path: "/salesperson", query: { tab: "orders" } });
    };
    const goBack2 = () => {
        router.back();
    };

    const handleStatusUpdate = async (newStatus) => {
        await orderStore.updateOrderStatus(orderId, newStatus);
        await orderStore.fetchOrderDetails(orderId);
    };
</script>

<template>
    <div class="p-4">
        <div
            class="md:p-4 max-w-3xl mx-auto text-sm md:bg-gray-50 w-full h-full rounded-xl"
        >
            <div class="flex items-center justify-between mb-4">
                <h1 class="text-lg font-semibold text-gray-700">
                    Order Details
                </h1>
                <button
                    v-if="authStore.getUserRole === 'salesperson'"
                    @click="goBack"
                    class="px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-full flex justify-center items-center gap-3"
                >
                    <i class="pi pi-arrow-left"></i> Back
                </button>
                <button
                    v-else
                    @click="goBack2"
                    class="px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-full flex justify-center items-center gap-3"
                >
                    <i class="pi pi-arrow-left"></i> Back
                </button>
            </div>

            <div
                class="mb-4 rounded p-4 bg-white shadow text-gray-700 text-sm space-y-2"
            >
                <h2 class="font-medium mb-2 text-orange-600">Order Details</h2>
                <p>
                    Status:
                    <span
                        :class="{
                            'text-yellow-500 px-2 py-1 rounded font-semibold':
                                orderStore.orderDetails?.status === 'PENDING',
                            'text-blue-500 px-2 py-1 rounded font-semibold':
                                orderStore.orderDetails?.status ===
                                'PROCESSING',
                            'text-green-500  px-2 py-1 rounded font-semibold':
                                orderStore.orderDetails?.status === 'DELIVERED',
                        }"
                    >
                        {{ orderStore.orderDetails?.status }}
                    </span>
                </p>
                <p>
                    Shipping Address:
                    <span class="text-gray-900 font-medium">{{
                        orderStore.orderDetails?.shipping_address
                    }}</span>
                </p>
                <p>
                    Total GH₵:
                    <span class="text-gray-900 font-medium">
                        {{ orderStore.orderDetails?.total_amount }}</span
                    >
                </p>

                <!-- Status-based Action Button -->
                <div
                    v-if="authStore.getUserRole === 'salesperson'"
                    class="mt-4"
                >
                    <button
                        v-if="orderStore.orderDetails?.status === 'PENDING'"
                        @click="handleStatusUpdate('PROCESSING')"
                        class="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-2 rounded-full flex justify-center items-center gap-3"
                    >
                        <i class="pi pi-check"></i> Processing
                    </button>

                    <button
                        v-if="orderStore.orderDetails?.status === 'PROCESSING'"
                        @click="handleStatusUpdate('DELIVERED')"
                        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-full flex justify-center items-center gap-3"
                    >
                        <i class="pi pi-check"></i> Delivered
                    </button>
                </div>
            </div>
            <div class="bg-white shadow rounded p-4 mb-4">
                <h2 class="font-medium mb-2 text-orange-600">
                    Item(s) in this Order
                </h2>
                <div class="overflow-x-auto">
                    <table
                        class="min-w-full table-auto bg-white rounded shadow"
                    >
                        <thead class="bg-gray-100 text-left">
                            <tr>
                                <th class="px-4 py-2 font-medium">Product</th>
                                <th class="px-4 py-2 font-medium">Quantity</th>
                                <th class="px-4 py-2 font-medium truncate">
                                    Unit (GH₵)
                                </th>
                                <th class="px-4 py-2 font-medium truncate">
                                    Total (GH₵)
                                </th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            <tr
                                v-for="item in orderStore.orderDetails
                                    ?.order_items"
                                :key="item.id"
                                class="hover:bg-gray-50"
                            >
                                <td class="px-4 py-2 truncate">
                                    {{ item.product.name }}
                                </td>
                                <td class="px-4 py-2">{{ item.quantity }}</td>
                                <td class="px-4 py-2">
                                    {{
                                        (
                                            parseFloat(item.amount) /
                                            item.quantity
                                        ).toFixed(2)
                                    }}
                                </td>
                                <td class="px-4 py-2">
                                    {{ parseFloat(item.amount).toFixed(2) }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <!-- Customer Details Section -->
            <div
                v-if="authStore.getUserRole === 'salesperson'"
                class="mb-4 rounded p-4 bg-white shadow space-y-2"
            >
                <h2 class="font-medium mb-2 text-orange-600">
                    Customer Details
                </h2>
                <p>
                    Name:
                    <span class="text-gray-900 font-medium">{{
                        orderStore.orderDetails?.customer?.profile
                            ? `${orderStore.orderDetails.customer.profile.first_name} ${orderStore.orderDetails.customer.profile.last_name}`
                            : "N/A"
                    }}</span>
                </p>
                <p>
                    Email:
                    <span class="text-gray-900 font-medium">{{
                        orderStore.orderDetails?.customer?.email || "N/A"
                    }}</span>
                </p>
                <p>
                    Phone:
                    <span class="text-gray-900 font-medium">{{
                        orderStore.orderDetails?.customer?.profile?.phone ||
                        "N/A"
                    }}</span>
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
