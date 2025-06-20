<script setup>
    import { computed, onMounted, ref } from "vue";
    import { useRoute, useRouter } from "vue-router";
    import { useOrderStore } from "@/stores/orderStore";
    import { useAuthStore } from "@/stores/auth";
    import {
        ArrowLeft,
        Package,
        Clock,
        MapPin,
        User,
        Phone,
        Mail,
        Calendar,
        CreditCard,
        CheckCircle,
        XCircle,
        AlertCircle,
        Truck,
        Star,
    } from "lucide-vue-next";
    import { useToast } from "vue-toastification";
    import Spinner from "../ui/Spinner.vue";

    const route = useRoute();
    const router = useRouter();
    const orderStore = useOrderStore();
    const authStore = useAuthStore();
    const toast = useToast();

    const orderId = route.params.id;
    const isLoading = ref(true);

    onMounted(async () => {
        try {
            await orderStore.fetchOrderDetails(orderId);
        } finally {
            isLoading.value = false;
        }
    });

    const order = computed(() => orderStore.orderDetails);

    const goBack = () => {
        if (authStore.user?.role === "salesperson") {
            router.push({ path: "/salesperson", query: { tab: "orders" } });
        } else {
            router.back();
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        });
    };

    const formatCurrency = (amount) => {
        return `₵${parseFloat(amount || 0).toFixed(2)}`;
    };

    const getStatusConfig = (status) => {
        const configs = {
            PENDING: {
                color: "bg-yellow-100 text-yellow-800 border-yellow-200",
                icon: Clock,
                iconColor: "text-yellow-600",
                description: "Your order is being prepared",
            },
            PROCESSING: {
                color: "bg-blue-100 text-blue-800 border-blue-200",
                icon: Package,
                iconColor: "text-blue-600",
                description: "Your order is being processed",
            },
            DELIVERED: {
                color: "bg-green-100 text-green-800 border-green-200",
                icon: CheckCircle,
                iconColor: "text-green-600",
                description: "Your order has been delivered",
            },
            CANCELLED: {
                color: "bg-red-100 text-red-800 border-red-200",
                icon: XCircle,
                iconColor: "text-red-600",
                description: "This order was cancelled",
            },
        };
        return (
            configs[status] || {
                color: "bg-gray-100 text-gray-800 border-gray-200",
                icon: AlertCircle,
                iconColor: "text-gray-600",
                description: "Order status unknown",
            }
        );
    };

    const statusConfig = computed(() => {
        return getStatusConfig(order.value?.status);
    });

    const canCancelOrder = computed(() => {
        const status = order.value?.status?.toLowerCase();
        return ["pending", "processing"].includes(status);
    });

    const handleCancelOrder = async () => {
        if (
            !confirm(
                "Are you sure you want to cancel this order? This action cannot be undone."
            )
        ) {
            return;
        }

        try {
            await orderStore.deleteOrder(orderId);
            toast.success("Order cancelled successfully.");
            goBack();
        } catch (error) {
            toast.error("Failed to cancel order.");
        }
    };

    const handleStatusUpdate = async (newStatus) => {
        try {
            await orderStore.updateOrderStatus(orderId, newStatus);
            await orderStore.fetchOrderDetails(orderId);
        } catch (error) {}
    };

    const getItemSubtotal = (item) => {
        const unitPrice = parseFloat(item.amount) / item.quantity;
        return unitPrice * item.quantity;
    };
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
                <div class="flex items-center justify-between py-4">
                    <button
                        @click="goBack"
                        class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-gray-400 transition-all duration-200 shadow-sm"
                    >
                        <ArrowLeft class="w-4 h-4" />
                        Back
                    </button>
                    <div>
                        <h1
                            class="text-xl font-styleScript bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent"
                        >
                            Order Details
                        </h1>
                    </div>
                    <!-- Spacer for centering -->
                </div>
            </div>
        </div>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Loading State -->
            <div v-if="isLoading" class="text-center py-16">
                <Spinner class="mx-auto mb-4" />
                <p class="text-gray-600 font-medium">
                    Loading order details...
                </p>
            </div>

            <!-- Error State -->
            <div
                v-else-if="orderStore.error"
                class="max-w-md mx-auto text-center py-16"
            >
                <div
                    class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4"
                >
                    <XCircle class="w-8 h-8 text-red-600" />
                </div>
                <h3 class="text-xl font-bold text-gray-800 mb-2">
                    Unable to load order
                </h3>
                <p class="text-gray-600 mb-6">{{ orderStore.error }}</p>
                <button
                    @click="goBack"
                    class="px-6 py-3 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg font-medium hover:from-orange-600 hover:to-orange-700 transition-all duration-200 shadow-md"
                >
                    Go Back
                </button>
            </div>

            <!-- Order Details -->
            <div v-else-if="order" class="space-y-8">
                <div
                    class="flex items-center justify-between p-4 -my-4 shadow rounded-xl bg-white"
                >
                    <h1 class="text-gray-600 font-medium">Payment Status</h1>
                    <p
                        class="capitalize font-medium text-white py-1 px-3 rounded-full bg-blue-500 w-max"
                    >
                        {{ order.payment_status }}
                    </p>
                </div>
                <!-- Order Header -->
                <div
                    class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden"
                >
                    <div
                        class="bg-gradient-to-r from-orange-50 to-red-50 px-6 py-4 border-b border-orange-100"
                    >
                        <div class="flex items-center justify-between">
                            <div>
                                <h2
                                    class="text-orange-700 flex items-center gap-3"
                                >
                                    <Package class="w-7 h-7" />
                                    #{{ order.id.slice(-4).toUpperCase() }}
                                </h2>
                                <p class="text-orange-600 text-sm mt-1">
                                    {{ formatDate(order.created_at) }}
                                </p>
                            </div>
                            <div class="text-right">
                                <div
                                    :class="[
                                        'inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold border',
                                        statusConfig.color,
                                    ]"
                                >
                                    <component
                                        :is="statusConfig.icon"
                                        class="w-4 h-4"
                                    />
                                    {{ order.status }}
                                </div>
                                <p class="text-sm text-gray-600 mt-1">
                                    {{ statusConfig.description }}
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Order Summary -->
                    <div class="p-6">
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div class="flex items-center gap-4">
                                <div
                                    class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center"
                                >
                                    <CreditCard
                                        class="w-6 h-6 text-green-600"
                                    />
                                </div>
                                <div>
                                    <p class="text-sm text-gray-600">
                                        Total Amount
                                    </p>
                                    <p
                                        class="text-xl font-semibold text-green-600"
                                    >
                                        {{
                                            formatCurrency(
                                                parseFloat(order.total_amount) +
                                                    15
                                            )
                                        }}
                                    </p>
                                </div>
                            </div>

                            <div class="flex items-center gap-4">
                                <div
                                    class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center"
                                >
                                    <Package class="w-6 h-6 text-blue-600" />
                                </div>
                                <div>
                                    <p class="text-sm text-gray-600">Items</p>
                                    <p
                                        class="text-xl font-semibold text-blue-500"
                                    >
                                        {{ order.order_items?.length || 0 }}
                                        item{{
                                            order.order_items?.length !== 1
                                                ? "s"
                                                : ""
                                        }}
                                    </p>
                                </div>
                            </div>

                            <div class="flex items-center gap-4">
                                <div
                                    class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center"
                                >
                                    <Truck class="w-6 h-6 text-purple-600" />
                                </div>
                                <div>
                                    <p class="text-sm text-gray-600">
                                        Order Type
                                    </p>
                                    <p
                                        class="text-xl font-semibold text-purple-600"
                                    >
                                        {{ order.order_type || "ONLINE" }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Order Items -->
                <div
                    class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden"
                >
                    <div
                        class="bg-gradient-to-r from-blue-50 to-indigo-50 px-6 py-4 border-b border-blue-100"
                    >
                        <h3
                            class="text-xl font-semibold text-blue-700 flex items-center gap-2"
                        >
                            <Package class="w-6 h-6" />
                            Order Items
                        </h3>
                        <p class="text-blue-600 text-sm mt-1">
                            Medications in your order
                        </p>
                    </div>

                    <div class="p-4">
                        <div class="space-y-2">
                            <div
                                v-for="item in order.order_items"
                                :key="item.id"
                                class="flex items-center gap-4 transition-colors"
                            >
                                <div
                                    class="w-16 h-16 bg-gradient-to-br from-orange-100 to-red-100 rounded-lg flex items-center justify-center flex-shrink-0"
                                >
                                    <Package class="w-8 h-8 text-orange-600" />
                                </div>

                                <div class="flex-1 min-w-0">
                                    <h4
                                        class="font-semibold text-gray-800 line-clamp-1"
                                    >
                                        {{
                                            item.product?.name ||
                                            "Unknown Product"
                                        }}
                                    </h4>
                                    <p
                                        class="text-sm text-gray-600 line-clamp-2 mt-1"
                                    >
                                        {{
                                            item.product?.description ||
                                            "No description available"
                                        }}
                                    </p>
                                    <div class="flex items-center gap-4 mt-3">
                                        <span class="text-sm text-gray-500"
                                            >Qty: {{ item.quantity }}</span
                                        >
                                        <span class="text-sm text-gray-500"
                                            >Unit:
                                            {{
                                                formatCurrency(
                                                    parseFloat(item.amount) /
                                                        item.quantity
                                                )
                                            }}</span
                                        >
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Order Total -->
                        <div class="mt-6 pt-6 border-t border-gray-200">
                            <div class="flex justify-between items-center">
                                <span class="font-medium text-gray-700"
                                    >Order Total</span
                                >
                                <span class="font-semibold text-green-600">{{
                                    formatCurrency(
                                        parseFloat(order.total_amount) + 15
                                    )
                                }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Delivery Information -->
                <div
                    class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden"
                >
                    <div
                        class="bg-gradient-to-r from-green-50 to-emerald-50 px-6 py-4 border-b border-green-100"
                    >
                        <h3
                            class="text-lg font-semibold text-green-700 flex items-center gap-2"
                        >
                            <MapPin class="w-6 h-6" />
                            Delivery Information
                        </h3>
                    </div>
                    <div class="p-6">
                        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            <div>
                                <h4 class="font-semibold text-gray-800 mb-3">
                                    Delivery Address
                                </h4>
                                <div class="bg-gray-50 rounded-lg p-4">
                                    <p class="text-gray-700 leading-relaxed">
                                        {{ order.shipping_address }}
                                    </p>
                                </div>
                            </div>

                            <!-- Customer Information (for salesperson) -->
                            <div
                                v-if="
                                    authStore.user?.role === 'salesperson' &&
                                    order.customer
                                "
                            >
                                <h4 class="font-semibold text-gray-800 mb-3">
                                    Customer Information
                                </h4>
                                <div class="space-y-3">
                                    <div class="flex items-center gap-3">
                                        <User class="w-5 h-5 text-gray-500" />
                                        <span class="text-gray-700">
                                            {{
                                                order.customer.profile
                                                    ? `${order.customer.profile.first_name} ${order.customer.profile.last_name}`
                                                    : "No name available"
                                            }}
                                        </span>
                                    </div>
                                    <div class="flex items-center gap-3">
                                        <Mail class="w-5 h-5 text-gray-500" />
                                        <span class="text-gray-700">{{
                                            order.customer.email || "No email"
                                        }}</span>
                                    </div>
                                    <div class="flex items-center gap-3">
                                        <Phone class="w-5 h-5 text-gray-500" />
                                        <span class="text-gray-700">{{
                                            order.customer.profile?.phone ||
                                            "No phone"
                                        }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Actions (for salesperson) -->
                <div
                    v-if="authStore.user?.role === 'salesperson'"
                    class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden"
                >
                    <div
                        class="bg-gradient-to-r from-orange-50 to-red-50 px-6 py-4 border-b border-orange-100"
                    >
                        <h3 class="text-xl font-bold text-orange-700">
                            Order Actions
                        </h3>
                        <p class="text-orange-600 text-sm mt-1">
                            Update order status
                        </p>
                    </div>

                    <div class="p-6">
                        <div class="flex flex-wrap gap-4">
                            <!-- Show Cancel button if unpaid -->
                            <button
                                v-if="order.payment_status === 'UNPAID'"
                                @click="handleCancelOrder"
                                class="px-6 py-3 bg-red-500 hover:bg-red-600 text-white rounded-lg font-medium transition-all duration-200 shadow-md hover:shadow-lg flex items-center gap-2"
                            >
                                <XCircle class="w-5 h-5" />
                                Cancel Order
                            </button>

                            <!-- Show normal status buttons if paid -->
                            <template v-else>
                                <button
                                    v-if="order.status === 'PENDING'"
                                    @click="handleStatusUpdate('PROCESSING')"
                                    class="px-6 py-3 bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg font-medium transition-all duration-200 shadow-md hover:shadow-lg flex items-center gap-2"
                                >
                                    <Clock class="w-5 h-5" />
                                    Mark as Processing
                                </button>

                                <button
                                    v-if="order.status === 'PROCESSING'"
                                    @click="handleStatusUpdate('DELIVERED')"
                                    class="px-6 py-3 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium transition-all duration-200 shadow-md hover:shadow-lg flex items-center gap-2"
                                >
                                    <CheckCircle class="w-5 h-5" />
                                    Mark as Delivered
                                </button>
                            </template>
                        </div>
                    </div>
                </div>

                <!-- Customer Actions -->
                <div
                    v-else-if="canCancelOrder"
                    class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden"
                >
                    <div
                        class="bg-gradient-to-r from-red-50 to-pink-50 px-6 py-4 border-b border-red-100"
                    >
                        <h3 class="text-xl font-semibold text-red-700">
                            Order Management
                        </h3>
                        <p class="text-red-600 text-sm mt-1">
                            Manage your order
                        </p>
                    </div>

                    <div class="p-6">
                        <div
                            class="bg-red-50 border border-red-200 rounded-lg p-4 mb-4"
                        >
                            <div class="flex items-start gap-3">
                                <AlertCircle
                                    class="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0"
                                />
                                <div>
                                    <h4 class="font-medium text-red-800">
                                        Cancel Order
                                    </h4>
                                    <p class="text-sm text-red-700 mt-1">
                                        Once cancelled, this action cannot be
                                        undone. You will need to place a new
                                        order.
                                    </p>
                                </div>
                            </div>
                        </div>

                        <button
                            @click="handleCancelOrder"
                            class="px-6 py-3 bg-red-500 hover:bg-red-600 text-white rounded-lg font-medium transition-all duration-200 shadow-md hover:shadow-lg flex items-center gap-2"
                        >
                            <XCircle class="w-5 h-5" />
                            Cancel Order
                        </button>
                    </div>
                </div>

                <!-- Order Timeline (for completed orders) -->
                <div
                    v-if="order.status === 'DELIVERED'"
                    class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden"
                >
                    <div
                        class="bg-gradient-to-r from-green-50 to-emerald-50 px-6 py-4 border-b border-green-100"
                    >
                        <h3
                            class="text-xl font-semibold text-green-700 flex items-center gap-2"
                        >
                            <CheckCircle class="w-6 h-6" />
                            Order Complete
                        </h3>
                    </div>

                    <div class="p-6">
                        <div class="flex items-center gap-4 text-green-600">
                            <CheckCircle class="w-8 h-8" />
                            <div>
                                <p class="font-semibold">
                                    Order Delivered Successfully
                                </p>
                                <p class="text-sm text-gray-600">
                                    Thank you for choosing Venella Pharmacy!
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- No Order Found -->
            <div v-else class="max-w-md mx-auto text-center py-16">
                <div
                    class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4"
                >
                    <Package class="w-8 h-8 text-gray-400" />
                </div>
                <h3 class="text-xl font-bold text-gray-800 mb-2">
                    Order not found
                </h3>
                <p class="text-gray-600 mb-6">
                    The order you're looking for doesn't exist or has been
                    removed.
                </p>
                <button
                    @click="goBack"
                    class="px-6 py-3 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg font-medium hover:from-orange-600 hover:to-orange-700 transition-all duration-200 shadow-md"
                >
                    Go Back
                </button>
            </div>
        </div>
    </div>
</template>
