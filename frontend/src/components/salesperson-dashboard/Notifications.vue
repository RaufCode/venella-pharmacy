<script setup>
    import { ref, computed, onMounted, onUnmounted } from "vue";
    import {
        Bell,
        Package,
        Truck,
        CheckCircle,
        Clock,
        AlertCircle,
        X,
        Filter,
        Search,
        ChevronDown,
    } from "lucide-vue-next";
    import { useNotificationStore } from "@/stores/notification";

    // Initialize the notification store
    const notificationStore = useNotificationStore();

    // Component state
    const activeFilter = ref("all");
    const searchTerm = ref("");
    const showMobileFilters = ref(false);

    // Icon mapping for notification types
    const iconMap = {
        NEW_ORDER: Package,
        ORDER_PROCESSING: Clock,
        ORDER_DELIVERED: CheckCircle,
        ORDER_CANCELLED: X,
        PAYMENT_RECEIVED: CheckCircle,
        STOCK_ALERT: AlertCircle,
        SYSTEM_UPDATE: Bell,
        PROMOTION: Bell,
        order: Package,
        delivery: Truck,
        completed: CheckCircle,
        reminder: Clock,
        alert: AlertCircle,
    };

    // Color mapping for notification types
    const colorMap = {
        NEW_ORDER: { text: "text-blue-500", bg: "bg-blue-50" },
        ORDER_PROCESSING: { text: "text-orange-500", bg: "bg-orange-50" },
        ORDER_DELIVERED: { text: "text-green-500", bg: "bg-green-50" },
        ORDER_CANCELLED: { text: "text-red-500", bg: "bg-red-50" },
        PAYMENT_RECEIVED: { text: "text-purple-500", bg: "bg-purple-50" },
        STOCK_ALERT: { text: "text-yellow-500", bg: "bg-yellow-50" },
        SYSTEM_UPDATE: { text: "text-gray-500", bg: "bg-gray-50" },
        PROMOTION: { text: "text-pink-500", bg: "bg-pink-50" },
        order: { text: "text-blue-500", bg: "bg-blue-50" },
        delivery: { text: "text-orange-500", bg: "bg-orange-50" },
        completed: { text: "text-green-500", bg: "bg-green-50" },
        reminder: { text: "text-purple-500", bg: "bg-purple-50" },
        alert: { text: "text-red-500", bg: "bg-red-50" },
    };

    // Computed properties using the store
    const notifications = computed(() => notificationStore.allNotifications);
    const unreadCount = computed(() => notificationStore.unreadCount);
    const isLoading = computed(() => notificationStore.isLoading);
    const error = computed(() => notificationStore.error);

    // Helper function to get notification icon
    const getNotificationIcon = (type) => {
        return iconMap[type] || Bell;
    };

    // Helper function to get notification colors
    const getNotificationColors = (type) => {
        return colorMap[type] || { text: "text-gray-500", bg: "bg-gray-50" };
    };

    // Helper function to format notification for display
    const formatNotification = (notification) => {
        const colors = getNotificationColors(notification.type);
        return {
            ...notification,
            icon: getNotificationIcon(notification.type),
            color: colors.text,
            bgColor: colors.bg,
            time: notificationStore.formatNotificationDate(
                notification.created_at
            ),
        };
    };

    // Filter options computed property
    const filterOptions = computed(() => {
        const typeFilters = [
            { key: "NEW_ORDER", label: "Orders" },
            { key: "ORDER_PROCESSING", label: "Processing" },
            { key: "ORDER_DELIVERED", label: "Delivered" },
            { key: "STOCK_ALERT", label: "Alerts" },
            { key: "PROMOTION", label: "Promotions" },
        ];

        const options = [
            { key: "all", label: "All", count: notifications.value.length },
        ];

        typeFilters.forEach((filter) => {
            const count = notificationStore.getNotificationsByType(
                filter.key
            ).length;
            if (count > 0) {
                options.push({ ...filter, count });
            }
        });

        return options;
    });

    // Filtered notifications computed property
    const filteredNotifications = computed(() => {
        let filtered = notifications.value;

        // Filter by type
        if (activeFilter.value !== "all") {
            filtered = notificationStore.getNotificationsByType(
                activeFilter.value
            );
        }

        // Filter by search term
        if (searchTerm.value) {
            const searchLower = searchTerm.value.toLowerCase();
            filtered = filtered.filter(
                (n) =>
                    n.title?.toLowerCase().includes(searchLower) ||
                    n.message?.toLowerCase().includes(searchLower)
            );
        }

        // Format notifications for display
        return filtered.map(formatNotification);
    });

    // Methods
    const markAsRead = async (id) => {
        try {
            await notificationStore.markAsRead(id);
        } catch (error) {
            console.error("Failed to mark notification as read:", error);
        }
    };

    const markAllAsRead = async () => {
        try {
            await notificationStore.markAllAsRead();
        } catch (error) {
            console.error("Failed to mark all notifications as read:", error);
        }
    };

    const deleteNotification = async (id) => {
        try {
            await notificationStore.deleteNotification(id);
        } catch (error) {
            console.error("Failed to delete notification:", error);
        }
    };

    const clearError = () => {
        notificationStore.clearError();
    };

    // Lifecycle hooks
    onMounted(() => {
        // Initialize the store - you might want to pass role and userId from props or auth store
        // For example: notificationStore.initialize('customer', userId);
        // For now, we'll just fetch notifications if store is already initialized
        if (notificationStore.role) {
            notificationStore.fetchNotifications();
        }
    });

    onUnmounted(() => {
        // Clean up polling when component is destroyed
        notificationStore.stopPolling();
    });

    // Props (optional - for initialization)
    const props = defineProps({
        role: {
            type: String,
            default: null,
            validator: (value) =>
                ["customer", "salesperson", null].includes(value),
        },
        userId: {
            type: [String, Number],
            default: null,
        },
    });

    // Initialize store if props are provided
    if (props.role) {
        notificationStore.initialize(props.role, props.userId);
    }
</script>

<template>
    <div class="min-h-screen">
        <!-- Error Message -->
        <div
            v-if="error"
            class="bg-red-50 border border-red-200 rounded-md p-4 mb-4"
        >
            <div class="flex">
                <div class="flex-shrink-0">
                    <AlertCircle class="h-5 w-5 text-red-400" />
                </div>
                <div class="ml-3">
                    <p class="text-sm text-red-800">{{ error }}</p>
                    <button
                        @click="clearError"
                        class="mt-2 text-sm text-red-600 hover:text-red-800 underline"
                    >
                        Dismiss
                    </button>
                </div>
            </div>
        </div>

        <!-- Loading Spinner -->
        <div v-if="isLoading" class="flex justify-center items-center py-8">
            <div
                class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"
            ></div>
        </div>

        <!-- Topbar -->
        <div
            class="bg-white shadow-sm border-b sticky top-0 z-40 hidden md:block"
        >
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex items-center justify-between h-16">
                    <div class="flex items-center space-x-4">
                        <div>
                            <h1 class="text-3xl font-styleScript text-gray-900">
                                Notifications Hub
                            </h1>
                        </div>
                    </div>
                    <button
                        v-if="unreadCount > 0"
                        @click="markAllAsRead"
                        class="text-sm text-blue-600 hover:text-blue-800 font-medium"
                        :disabled="isLoading"
                    >
                        Mark all as read
                    </button>
                </div>
            </div>
        </div>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div class="flex flex-col lg:flex-row gap-6">
                <!-- Filters Sidebar (desktop) -->
                <div class="lg:w-64 flex-shrink-0 hidden lg:block">
                    <div
                        class="bg-white rounded-lg shadow-sm border p-4 sticky top-24"
                    >
                        <h3
                            class="font-semibold text-gray-900 mb-4 flex items-center"
                        >
                            <Filter class="h-4 w-4 mr-2" /> Filters
                        </h3>
                        <div class="relative mb-4">
                            <Search
                                class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400"
                            />
                            <input
                                v-model="searchTerm"
                                placeholder="Search notifications..."
                                class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:border-orange-700"
                            />
                        </div>
                        <div class="space-y-2">
                            <button
                                v-for="option in filterOptions"
                                :key="option.key"
                                @click="activeFilter = option.key"
                                class="w-full flex items-center justify-between px-3 py-2 rounded-lg text-left transition-colors"
                                :class="
                                    activeFilter === option.key
                                        ? 'bg-blue-50 text-blue-700 border border-blue-200'
                                        : 'hover:bg-gray-50 text-gray-700'
                                "
                            >
                                <span class="font-medium">{{
                                    option.label
                                }}</span>
                                <span
                                    :class="
                                        activeFilter === option.key
                                            ? 'bg-blue-100 text-blue-700'
                                            : 'bg-gray-100 text-gray-600'
                                    "
                                    class="text-xs px-2 py-1 rounded-full"
                                >
                                    {{ option.count }}
                                </span>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Accordion Filter (mobile/tablet) -->
                <div class="lg:hidden">
                    <button
                        @click="showMobileFilters = !showMobileFilters"
                        class="flex items-center justify-between w-full px-4 py-3 bg-white border rounded-lg shadow-sm text-sm font-medium text-gray-700"
                    >
                        <span
                            ><Filter class="inline h-4 w-4 mr-2" />
                            Filters</span
                        >
                        <ChevronDown class="h-4 w-4" />
                    </button>
                    <div
                        v-if="showMobileFilters"
                        class="bg-white mt-2 p-4 rounded-lg border shadow-sm"
                    >
                        <div class="relative mb-4">
                            <Search
                                class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400"
                            />
                            <input
                                v-model="searchTerm"
                                placeholder="Search notifications..."
                                class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                        </div>
                        <div class="space-y-2">
                            <button
                                v-for="option in filterOptions"
                                :key="option.key"
                                @click="activeFilter = option.key"
                                class="w-full flex items-center justify-between px-3 py-2 rounded-lg text-left transition-colors"
                                :class="
                                    activeFilter === option.key
                                        ? 'bg-blue-50 text-blue-700 border border-blue-200'
                                        : 'hover:bg-gray-50 text-gray-700'
                                "
                            >
                                <span class="font-medium">{{
                                    option.label
                                }}</span>
                                <span
                                    :class="
                                        activeFilter === option.key
                                            ? 'bg-blue-100 text-blue-700'
                                            : 'bg-gray-100 text-gray-600'
                                    "
                                    class="text-xs px-2 py-1 rounded-full"
                                >
                                    {{ option.count }}
                                </span>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Notification List -->
                <div class="flex-1">
                    <div
                        v-if="filteredNotifications.length === 0 && !isLoading"
                        class="bg-white rounded-lg shadow-sm border p-8 text-center"
                    >
                        <Bell class="h-12 w-12 text-gray-400 mx-auto mb-4" />
                        <h3 class="text-lg font-medium text-gray-900 mb-2">
                            No notifications found
                        </h3>
                        <p class="text-gray-500">
                            {{
                                searchTerm
                                    ? "Try adjusting your search terms."
                                    : "You're all caught up!"
                            }}
                        </p>
                    </div>

                    <div v-else class="space-y-3">
                        <div
                            v-for="n in filteredNotifications"
                            :key="n.id"
                            class="bg-white rounded-lg shadow-sm border hover:shadow-md transition-all"
                            :class="{ 'border-l-4 border-l-blue-500': !n.read }"
                        >
                            <div class="p-4 sm:p-6">
                                <div
                                    class="flex gap-4 items-start sm:items-center sm:space-x-4 space-y-2 sm:space-y-0"
                                >
                                    <div
                                        :class="`flex-shrink-0 w-10 h-10 rounded-full ${n.bgColor} flex items-center justify-center`"
                                    >
                                        <component
                                            :is="n.icon"
                                            :class="`h-5 w-5 ${n.color}`"
                                        />
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <h4
                                            :class="`text-sm font-medium ${
                                                !n.read
                                                    ? 'text-gray-900'
                                                    : 'text-gray-700'
                                            }`"
                                        >
                                            {{ n.title }}
                                        </h4>
                                        <p
                                            class="text-sm text-gray-600 mt-1 leading-relaxed"
                                        >
                                            {{ n.message }}
                                        </p>
                                        <!-- Time & Mark as Read below on mobile -->
                                        <div
                                            class="mt-2 flex flex-col sm:flex-row sm:justify-between sm:items-center"
                                        >
                                            <p class="text-xs text-gray-400">
                                                {{ n.time }}
                                            </p>
                                            <div
                                                class="flex items-center space-x-2 mt-2 sm:mt-0"
                                            >
                                                <button
                                                    v-if="!n.read"
                                                    @click="markAsRead(n.id)"
                                                    class="text-xs text-blue-600 hover:text-blue-800 font-medium"
                                                    :disabled="
                                                        notificationStore
                                                            .markingAsRead[n.id]
                                                    "
                                                >
                                                    {{
                                                        notificationStore
                                                            .markingAsRead[n.id]
                                                            ? "Marking..."
                                                            : "Mark read"
                                                    }}
                                                </button>
                                                <button
                                                    @click="
                                                        deleteNotification(n.id)
                                                    "
                                                    class="text-gray-400 hover:text-red-500 transition-colors"
                                                >
                                                    <X class="h-4 w-4" />
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
