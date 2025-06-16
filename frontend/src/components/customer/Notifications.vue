<script setup>
    import { ArrowLeft, Bell, Search, Trash2 } from "lucide-vue-next";
    import { computed, ref, onMounted, onUnmounted } from "vue";
    import { useNotificationStore } from "@/stores/notification";

    const goBack = () => {
        window.history.back();
    };

    const notificationStore = useNotificationStore();
    const searchTerm = ref("");

    // Unread count for red bubble
    const unreadCount = computed(() => notificationStore.unreadCount);

    // Filtered notifications based on search
    const filteredNotifications = computed(() => {
        const term = searchTerm.value.toLowerCase();
        return notificationStore.notifications.filter((n) =>
            n.content.toLowerCase().includes(term)
        );
    });

    // Mark all visible notifications as read
    const markAll = () => {
        filteredNotifications.value.forEach((notif) => {
            if (!notif.read) {
                notificationStore.markAsRead(notif.id);
            }
        });
    };

    // Delete handler
    const deleteNotification = async (id) => {
        const confirmDelete = confirm("Delete this notification?");
        if (!confirmDelete) return;

        try {
            await notificationStore.deleteNotification(id);
        } catch (error) {
            console.error("Failed to delete notification", error);
        }
    };

    // Format date and time
    function formatDateTime(datetime) {
        const date = new Date(datetime);
        return {
            date: date.toLocaleDateString(),
            time: date.toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
            }),
        };
    }

    // Start/stop polling
    onMounted(() => {
        notificationStore.startPolling();
    });
    onUnmounted(() => {
        notificationStore.stopPolling();
    });
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
                        class="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-gray-400 transition-all duration-200 shadow-sm"
                    >
                        <ArrowLeft class="w-4 h-4" />
                        Back
                    </button>

                    <!-- Title and Bell with Bubble -->
                    <div class="flex items-center gap-3">
                        <div>
                            <h1
                                class="text-xl font-styleScript bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent hidden md:block"
                            >
                                Notifications
                            </h1>
                        </div>
                    </div>

                    <!-- Mark All Button -->
                    <button
                        @click="markAll"
                        :disabled="unreadCount === 0"
                        class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-full hover:from-blue-700 hover:to-indigo-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transition-all duration-200 shadow-sm"
                    >
                        <svg
                            class="w-4 h-4"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M5 13l4 4L19 7"
                            ></path>
                        </svg>
                        Mark all
                    </button>
                </div>
            </div>
        </div>

        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Search Input -->
            <div class="mb-8">
                <div class="relative max-w-xl mx-auto">
                    <Search
                        class="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400"
                    />
                    <input
                        v-model="searchTerm"
                        placeholder="Search your notifications..."
                        class="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl text-gray-800 placeholder-gray-500 focus:border-orange-500 transition-all duration-200 bg-white shadow-sm"
                    />
                </div>
            </div>

            <!-- Loading State -->
            <div v-if="notificationStore.loading" class="text-center py-16">
                <div
                    class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-orange-100 to-red-100 rounded-full mb-4"
                >
                    <div
                        class="w-8 h-8 border-4 border-orange-200 border-t-orange-600 rounded-full animate-spin"
                    ></div>
                </div>
                <p class="text-gray-600 font-medium">
                    Loading notifications...
                </p>
            </div>

            <!-- Empty State -->
            <div
                v-else-if="filteredNotifications.length === 0"
                class="text-center py-16"
            >
                <div class="max-w-md mx-auto">
                    <div
                        class="w-24 h-24 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto mb-6"
                    >
                        <Bell class="w-12 h-12 text-gray-400" />
                    </div>
                    <h3 class="text-2xl font-bold text-gray-800 mb-4">
                        {{
                            searchTerm
                                ? "No matching notifications"
                                : "No notifications yet"
                        }}
                    </h3>
                    <p class="text-gray-600 mb-8">
                        {{
                            searchTerm
                                ? "Try adjusting your search terms."
                                : "When you receive notifications, they will appear here."
                        }}
                    </p>
                    <button
                        v-if="searchTerm"
                        @click="searchTerm = ''"
                        class="bg-gradient-to-r from-orange-600 to-red-600 text-white px-6 py-3 rounded-xl hover:from-orange-700 hover:to-red-700 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 font-medium"
                    >
                        Clear Search
                    </button>
                </div>
            </div>

            <!-- Notifications List -->
            <div v-else class="space-y-4">
                <!-- Summary Stats -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                    <!-- Total Notifications -->
                    <div
                        class="bg-white rounded-xl p-4 shadow border border-gray-100"
                    >
                        <div class="flex items-center justify-between gap-3">
                            <div
                                class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center"
                            >
                                <Bell class="w-5 h-5 text-blue-600" />
                            </div>
                            <div class="text-right">
                                <p class="text-lg font-bold text-gray-800">
                                    {{ notificationStore.notifications.length }}
                                </p>
                                <p class="text-sm text-gray-600 font-semibold">
                                    Total
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Unread Notifications -->
                    <div
                        class="bg-white rounded-xl p-4 shadow border border-gray-100"
                    >
                        <div class="flex items-center justify-between gap-3">
                            <div
                                class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center"
                            >
                                <div
                                    class="w-2.5 h-2.5 bg-red-600 rounded-full"
                                ></div>
                            </div>
                            <div class="text-right">
                                <p class="text-lg font-bold text-gray-800">
                                    {{ unreadCount }}
                                </p>
                                <p class="text-sm text-gray-600 font-semibold">
                                    Unread
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Read Notifications -->
                    <div
                        class="bg-white rounded-xl p-4 shadow border border-gray-100"
                    >
                        <div class="flex items-center justify-between gap-3">
                            <div
                                class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center"
                            >
                                <svg
                                    class="w-5 h-5 text-green-600"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M5 13l4 4L19 7"
                                    ></path>
                                </svg>
                            </div>
                            <div class="text-right">
                                <p class="text-lg font-bold text-gray-800">
                                    {{
                                        notificationStore.notifications.length -
                                        unreadCount
                                    }}
                                </p>
                                <p class="text-sm text-gray-600 font-semibold">
                                    Read
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Filtered or Searched Notifications -->
                    <div
                        class="bg-white rounded-xl p-4 shadow border border-gray-100"
                    >
                        <div class="flex items-center justify-between gap-3">
                            <div
                                class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center"
                            >
                                <svg
                                    class="w-5 h-5 text-orange-600"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m-9 3v10a2 2 0 002 2h6a2 2 0 002-2V7H7z"
                                    ></path>
                                </svg>
                            </div>
                            <div class="text-right">
                                <p class="text-lg font-bold text-gray-800">
                                    {{ filteredNotifications.length }}
                                </p>
                                <p class="text-sm text-gray-600 font-semibold">
                                    {{ searchTerm ? "Found" : "Showing" }}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Notification Cards -->
                <div class="space-y-3">
                    <div
                        v-for="notification in filteredNotifications"
                        :key="notification.id"
                        class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-all duration-200"
                        :class="{
                            'ring-2 ring-orange-200 border-orange-300':
                                !notification.read,
                        }"
                    >
                        <div class="p-4">
                            <!-- Header -->
                            <div>
                                <div
                                    class="flex items-center justify-between mb-2"
                                >
                                    <div class="flex items-center gap-3">
                                        <Bell class="w-5 h-5 text-orange-600" />
                                        <h3
                                            class="font-semibold text-gray-800 capitalize"
                                        >
                                            {{ notification.type }}
                                        </h3>
                                    </div>
                                    <div class="flex items-center gap-3">
                                        <span
                                            v-if="!notification.read"
                                            class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 animate-pulse"
                                        >
                                            <div
                                                class="w-1.5 h-1.5 bg-red-600 rounded-full mr-1.5"
                                            ></div>
                                            New
                                        </span>
                                        <div class="flex items-center gap-2">
                                            <button
                                                @click="
                                                    deleteNotification(
                                                        notification.id
                                                    )
                                                "
                                                class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                                                title="Delete notification"
                                            >
                                                <Trash2
                                                    class="w-4 h-4 text-yellow-500"
                                                />
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Content -->
                            <div class="mb-2">
                                <p
                                    class="text-gray-700 leading-relaxed text-justify text-sm"
                                >
                                    {{ notification.content }}
                                </p>
                            </div>
                            <div class="flex items-center">
                                <div class="flex items-center gap-2 mb-2">
                                    <span class="text-xs text-gray-500">{{
                                        formatDateTime(notification.created_at)
                                            .date
                                    }}</span>
                                    <span class="text-xs text-gray-500">{{
                                        formatDateTime(notification.created_at)
                                            .time
                                    }}</span>
                                </div>
                            </div>
                            <!-- Actions -->
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-3">
                                    <button
                                        v-if="!notification.read"
                                        @click="
                                            notificationStore.markAsRead(
                                                notification.id
                                            )
                                        "
                                        class="inline-flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
                                    >
                                        <svg
                                            class="w-4 h-4"
                                            fill="none"
                                            stroke="currentColor"
                                            viewBox="0 0 24 24"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M5 13l4 4L19 7"
                                            ></path>
                                        </svg>
                                        Mark as read
                                    </button>
                                    <span
                                        v-else
                                        class="inline-flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-green-600 bg-green-50 rounded-lg"
                                    >
                                        <svg
                                            class="w-4 h-4"
                                            fill="none"
                                            stroke="currentColor"
                                            viewBox="0 0 24 24"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M5 13l4 4L19 7"
                                            ></path>
                                        </svg>
                                        Read
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
>
