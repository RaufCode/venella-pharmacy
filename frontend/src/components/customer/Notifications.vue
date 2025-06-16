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
    <div class="relative w-full min-h-screen bg-gray-100">
        <!-- Header -->
        <div
            class="flex items-center p-4 justify-between shadow fixed top-0 z-50 w-full bg-white"
        >
            <button><ArrowLeft @click="goBack" /></button>

            <!-- Title and Bell with Bubble -->
            <div class="relative flex items-center space-x-2">
                <h1 class="font-medium">Notifications</h1>
                <div class="relative">
                    <Bell class="w-5 h-5 text-gray-600" />
                    <span
                        v-if="unreadCount > 0"
                        class="absolute -top-1 -right-1 h-2 w-2 bg-red-500 rounded-full"
                    ></span>
                </div>
            </div>

            <!-- Mark All -->
            <h1
                class="text-xs py-2 px-3 rounded-full bg-blue-500 text-white cursor-pointer"
                @click="markAll"
            >
                Mark all
            </h1>
        </div>

        <!-- Main Content -->
        <div
            class="flex flex-col items-center justify-center pt-20 container mx-auto p-4"
        >
            <!-- Search Input -->
            <div class="w-full max-w-xl">
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
            </div>

            <!-- Notifications List -->
            <div
                v-for="notification in filteredNotifications"
                :key="notification.id"
                class="max-w-xl text-justify shadow p-4 mb-2 bg-white rounded w-full"
            >
                <div class="flex items-center mb-4 justify-between">
                    <div class="flex items-center space-x-2">
                        <Bell class="w-4 h-4 text-gray-500" />
                        <h1
                            class="font-semibold capitalize text-gray-700 text-sm"
                        >
                            {{ notification.type }}
                        </h1>
                    </div>
                    <span
                        v-if="!notification.read"
                        class="text-xs py-1 px-2 rounded-full bg-red-500 text-white"
                    >
                        new
                    </span>
                </div>

                <div>
                    <p class="text-gray-600 text-sm">
                        {{ notification.content }}
                    </p>
                    <p class="text-xs mt-1 text-gray-400 flex space-x-2">
                        <span>{{
                            formatDateTime(notification.created_at).date
                        }}</span>
                        <span>{{
                            formatDateTime(notification.created_at).time
                        }}</span>
                    </p>
                    <div>
                        <button
                            v-if="!notification.read"
                            class="mt-2 p-1 text-sm text-blue-500 hover:underline"
                            @click="
                                notificationStore.markAsRead(notification.id)
                            "
                        >
                            Mark as read
                        </button>
                        <button
                            class="mt-2 p-1 text-sm text-red-500 hover:underline"
                            @click="deleteNotification(notification.id)"
                        >
                            <Trash2 class="h-4 w-4" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
>
