<script setup>
    import { ref, computed } from "vue";
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

    const activeFilter = ref("all");
    const searchTerm = ref("");
    const showMobileFilters = ref(false);

    const notifications = ref([
        {
            id: 1,
            type: "order",
            title: "Order Confirmed",
            message:
                "Your order #PH-2024-001 has been confirmed and is being prepared.",
            time: "2 mins ago",
            read: false,
            icon: Package,
            color: "text-blue-500",
            bgColor: "bg-blue-50",
        },
        {
            id: 2,
            type: "delivery",
            title: "Out for Delivery",
            message:
                "Your medication order is out for delivery. Expected arrival: 3:00 PM",
            time: "15 mins ago",
            read: false,
            icon: Truck,
            color: "text-orange-500",
            bgColor: "bg-orange-50",
        },
        {
            id: 3,
            type: "completed",
            title: "Order Delivered",
            message: "Order #PH-2024-002 has been successfully delivered.",
            time: "1 hour ago",
            read: true,
            icon: CheckCircle,
            color: "text-green-500",
            bgColor: "bg-green-50",
        },
        {
            id: 4,
            type: "reminder",
            title: "Prescription Reminder",
            message: "Time to take your evening medication - Metformin 500mg",
            time: "2 hours ago",
            read: false,
            icon: Clock,
            color: "text-purple-500",
            bgColor: "bg-purple-50",
        },
        {
            id: 5,
            type: "alert",
            title: "Low Stock Alert",
            message:
                "Your prescribed medication is running low. Consider reordering.",
            time: "3 hours ago",
            read: true,
            icon: AlertCircle,
            color: "text-red-500",
            bgColor: "bg-red-50",
        },
    ]);

    const unreadCount = computed(
        () => notifications.value.filter((n) => !n.read).length
    );

    const filterOptions = computed(() => [
        { key: "all", label: "All", count: notifications.value.length },
        {
            key: "order",
            label: "Orders",
            count: notifications.value.filter((n) => n.type === "order").length,
        },
        {
            key: "delivery",
            label: "Delivery",
            count: notifications.value.filter((n) => n.type === "delivery")
                .length,
        },
        {
            key: "reminder",
            label: "Reminders",
            count: notifications.value.filter((n) => n.type === "reminder")
                .length,
        },
        {
            key: "alert",
            label: "Alerts",
            count: notifications.value.filter((n) => n.type === "alert").length,
        },
    ]);

    const filteredNotifications = computed(() =>
        notifications.value.filter(
            (n) =>
                (activeFilter.value === "all" ||
                    n.type === activeFilter.value) &&
                (n.title
                    .toLowerCase()
                    .includes(searchTerm.value.toLowerCase()) ||
                    n.message
                        .toLowerCase()
                        .includes(searchTerm.value.toLowerCase()))
        )
    );

    const markAsRead = (id) => {
        const n = notifications.value.find((n) => n.id === id);
        if (n) n.read = true;
    };

    const markAllAsRead = () => {
        notifications.value.forEach((n) => (n.read = true));
    };

    const deleteNotification = (id) => {
        notifications.value = notifications.value.filter((n) => n.id !== id);
    };
</script>

<template>
    <div class="min-h-screen">
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
                        v-if="filteredNotifications.length === 0"
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
                                        :class="` flex-shrink-0 w-10 h-10 rounded-full ${n.bgColor} flex items-center justify-center`"
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
                                                >
                                                    Mark read
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
