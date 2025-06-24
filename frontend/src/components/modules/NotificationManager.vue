<script setup>
    import { ref, computed, onMounted } from "vue";
    import {
        Bell,
        AlertCircle,
        Clock,
        RefreshCw,
        ChevronLeft,
        ChevronRight,
        ShoppingCart,
        Package,
        User,
        Settings,
        Info,
    } from "lucide-vue-next";

    import BaseCard from "@/components/shared/BaseCard.vue";
    import BaseButton from "@/components/shared/BaseButton.vue";

    import { useNotificationStore } from "@/stores/notification";
    import { useAuthStore } from "@/stores/auth";

    const notificationStore = useNotificationStore();
    const authStore = useAuthStore();

    const activeFilter = ref("all");
    const currentPage = ref(1);
    const itemsPerPage = 10;

    const isLoading = computed(() => notificationStore.loading);
    const notifications = computed(() => notificationStore.notifications || []);
    const unreadCount = computed(() => notificationStore.unreadCount || 0);

    const todayCount = computed(() => {
        const today = new Date().toDateString();
        return notifications.value.filter(
            (notification) =>
                new Date(notification.created_at).toDateString() === today
        ).length;
    });

    const notificationFilters = computed(() => [
        { key: "all", label: "All", count: notifications.value.length },
        { key: "unread", label: "Unread", count: unreadCount.value },
        {
            key: "orders",
            label: "Orders",
            count: notifications.value.filter((n) => n.type === "order").length,
        },
        {
            key: "stock",
            label: "Stock",
            count: notifications.value.filter((n) => n.type === "stock").length,
        },
        {
            key: "system",
            label: "System",
            count: notifications.value.filter((n) => n.type === "system")
                .length,
        },
    ]);

    const filteredNotifications = computed(() => {
        let filtered = [...notifications.value];

        switch (activeFilter.value) {
            case "unread":
                filtered = filtered.filter((n) => !n.read);
                break;
            case "orders":
                filtered = filtered.filter((n) => n.type === "order");
                break;
            case "stock":
                filtered = filtered.filter((n) => n.type === "stock");
                break;
            case "system":
                filtered = filtered.filter((n) => n.type === "system");
                break;
        }

        return filtered.sort(
            (a, b) => new Date(b.created_at) - new Date(a.created_at)
        );
    });

    const totalPages = computed(() =>
        Math.ceil(filteredNotifications.value.length / itemsPerPage)
    );

    const paginatedNotifications = computed(() => {
        const start = (currentPage.value - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        return filteredNotifications.value.slice(start, end);
    });

    const getNotificationIcon = (type) => {
        switch (type) {
            case "order":
                return ShoppingCart;
            case "stock":
                return Package;
            case "user":
                return User;
            case "system":
                return Settings;
            default:
                return Info;
        }
    };

    const getNotificationIconStyle = (type) => {
        switch (type) {
            case "order":
                return "bg-blue-100 text-blue-600";
            case "stock":
                return "bg-red-100 text-red-600";
            case "user":
                return "bg-green-100 text-green-600";
            case "system":
                return "bg-purple-100 text-purple-600";
            default:
                return "bg-gray-100 text-gray-600";
        }
    };

    const formatTime = (dateString) => {
        const date = new Date(dateString);
        const now = new Date();
        const diff = now - date;

        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);

        if (minutes < 1) return "Just now";
        if (minutes < 60) return `${minutes}m ago`;
        if (hours < 24) return `${hours}h ago`;
        if (days < 7) return `${days}d ago`;

        return date.toLocaleDateString();
    };

    const markAsRead = async (notificationId) => {
        try {
            await notificationStore.markAsRead(notificationId);
        } catch (error) {
            console.error("Failed to mark notification as read:", error);
        }
    };

    const markAllAsRead = async () => {
        const unreadNotifications = notifications.value.filter((n) => !n.read);
        try {
            await Promise.all(
                unreadNotifications.map((n) =>
                    notificationStore.markAsRead(n.id)
                )
            );
        } catch (error) {
            console.error("Failed to mark all notifications as read:", error);
        }
    };

    const refreshNotifications = async () => {
        try {
            await notificationStore.fetchNotifications();
        } catch (error) {
            console.error("Failed to refresh notifications:", error);
        }
    };

    onMounted(() => {
        if (authStore.isAuthenticated) {
            notificationStore.fetchNotifications();
        }
    });
</script>
<template>
    <div class="space-y-6">
        <!-- Header -->
        <div
            class="flex flex-col lg:flex-row lg:items-center justify-between gap-4"
        >
            <div>
                <h2 class="text-xl text-gray-600">Notifications</h2>
            </div>

            <div>
                <BaseButton
                    variant="outline"
                    size="sm"
                    @click="markAllAsRead"
                    :disabled="unreadCount === 0"
                >
                    Mark All
                </BaseButton>
            </div>
        </div>

        <!-- Notification Stats -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div class="bg-white rounded-lg border border-gray-200 p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-600">Total Notifications</p>
                        <p class="text-2xl font-semibold text-gray-900 mt-1">
                            {{ notifications.length }}
                        </p>
                    </div>
                    <div
                        class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center"
                    >
                        <Bell class="w-5 h-5 text-blue-600" />
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg border border-gray-200 p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-600">Unread</p>
                        <p class="text-2xl font-semibold text-gray-900 mt-1">
                            {{ unreadCount }}
                        </p>
                    </div>
                    <div
                        class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center"
                    >
                        <AlertCircle class="w-5 h-5 text-red-600" />
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg border border-gray-200 p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-600">Today</p>
                        <p class="text-2xl font-semibold text-gray-900 mt-1">
                            {{ todayCount }}
                        </p>
                    </div>
                    <div
                        class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center"
                    >
                        <Clock class="w-5 h-5 text-green-600" />
                    </div>
                </div>
            </div>
        </div>

        <!-- Notification Filters -->
        <BaseCard>
            <template #header>
                <div class="flex gap-2 overflow-x-auto">
                    <button
                        v-for="filter in notificationFilters"
                        :key="filter.key"
                        @click="activeFilter = filter.key"
                        :class="[
                            'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
                            activeFilter === filter.key
                                ? 'bg-orange-100 text-orange-700 border border-orange-200'
                                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100',
                        ]"
                    >
                        {{ filter.label }}
                        <span
                            v-if="filter.count !== undefined"
                            class="ml-0 md:ml-2 text-xs opacity-75"
                        >
                            {{ filter.count }}
                        </span>
                    </button>
                </div>
            </template>

            <!-- Notifications List -->
            <div
                v-if="isLoading"
                class="flex items-center justify-center py-12"
            >
                <div
                    class="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"
                ></div>
            </div>

            <div
                v-else-if="filteredNotifications.length === 0"
                class="text-center py-12"
            >
                <Bell class="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <h3 class="text-lg font-medium text-gray-900">
                    No notifications
                </h3>
                <p class="text-gray-500">
                    You're all caught up! Check back later for new updates.
                </p>
            </div>

            <div v-else class="space-y-3">
                <div
                    v-for="notification in paginatedNotifications"
                    :key="notification.id"
                    :class="[
                        'flex items-start gap-4 p-4 rounded-lg border transition-colors cursor-pointer',
                        notification.read
                            ? 'bg-white border-gray-200 hover:bg-gray-50'
                            : 'bg-orange-50 border-orange-200 hover:bg-orange-100',
                    ]"
                    @click="markAsRead(notification.id)"
                >
                    <!-- Icon -->
                    <div
                        :class="[
                            'w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0',
                            getNotificationIconStyle(notification.type),
                        ]"
                    >
                        <component
                            :is="getNotificationIcon(notification.type)"
                            class="w-5 h-5"
                        />
                    </div>

                    <!-- Content -->
                    <div class="flex-1 min-w-0">
                        <div class="flex items-start justify-between gap-3">
                            <div class="flex-1">
                                <h4 class="text-sm font-medium text-gray-900">
                                    {{ notification.type }}
                                </h4>
                                <p
                                    class="text-sm text-gray-600 mt-1 break-words"
                                >
                                    {{ notification.content }}
                                </p>
                                <div class="mt-2 text-xs text-gray-500">
                                    {{ formatTime(notification.created_at) }}
                                </div>
                            </div>

                            <!-- Unread indicator -->
                            <div
                                v-if="!notification.read"
                                class="w-2 h-2 bg-orange-500 rounded-full flex-shrink-0 mt-2"
                            ></div>
                        </div>
                    </div>
                </div>

                <!-- Pagination -->
                <div v-if="totalPages > 1" class="mt-6">
                    <div class="flex items-center gap-2 w-max mx-auto">
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
