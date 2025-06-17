<script setup>
    import { ref, computed, onMounted, onUnmounted, watch } from "vue";
    import { useRoute, useRouter } from "vue-router";
    import {
        Home,
        Pill,
        ShoppingCart,
        TrendingUp,
        Users,
        Bell,
        Package,
        CheckCircle,
        AlertCircle,
        Clock,
    } from "lucide-vue-next";

    import BaseLayout from "@/components/shared/BaseLayout.vue";
    import NavigationMenu from "@/components/shared/NavigationMenu.vue";
    import StatsGrid from "@/components/shared/StatsGrid.vue";
    import MedicationManager from "@/components/modules/MedicationManager.vue";
    import OrderManager from "@/components/modules/OrderManager.vue";
    import SalesManager from "@/components/modules/SalesManager.vue";
    import StaffManager from "@/components/modules/StaffManager.vue";
    import NotificationManager from "@/components/modules/NotificationManager.vue";

    import { useAuthStore } from "@/stores/auth";
    import { useOrderStore } from "@/stores/orderStore";
    import { useNotificationStore } from "@/stores/notification";
    import { useMedStore } from "@/stores/medStore";

    const route = useRoute();
    const router = useRouter();

    const authStore = useAuthStore();
    const orderStore = useOrderStore();
    const notificationStore = useNotificationStore();
    const medStore = useMedStore();

    const activeTab = ref(route.query.tab || "overview");
    const sidebarOpen = ref(false);

    // User info
    const userName = computed(
        () => authStore.user?.profile?.first_name || "User"
    );
    const userRole = computed(() => authStore.user?.role || "user");

    // Navigation items based on role
    const navigationItems = computed(() => {
        const baseItems = [
            {
                key: "overview",
                label: "Overview",
                icon: Home,
            },
            {
                key: "medication",
                label: "Medications",
                icon: Pill,
            },
            {
                key: "orders",
                label: "Orders",
                icon: ShoppingCart,
                badge: orderStore.pendingOrders?.length || 0,
            },
            {
                key: "sales",
                label: "Sales",
                icon: TrendingUp,
            },
            {
                key: "notifications",
                label: "Notifications",
                icon: Bell,
                badge: notificationStore.unreadCount || 0,
            },
        ];

        // Add staff management for admin
        if (userRole.value === "admin") {
            baseItems.splice(4, 0, {
                key: "staff",
                label: "Staff",
                icon: Users,
            });
        }

        return baseItems;
    });

    // Page titles
    const pageTitle = computed(() => {
        const titles = {
            overview: "Dashboard",
            medication: "Medication Hub",
            orders: "Orders Hub",
            sales: "Sales Hub",
            staff: "Staff Hub",
            notifications: "Notification Hub",
        };
        return titles[activeTab.value] || "Dashboard";
    });

    // Notification count
    const notificationCount = computed(
        () => notificationStore.unreadCount || 0
    );

    // Overview stats
    const overviewStats = computed(() => {
        return [
            {
                label: "Orders",
                value: orderStore.orders?.length || 0,
                change: "+5%",
                changeType: "increase",
                icon: ShoppingCart,
                bgColor: "bg-blue-100",
                iconColor: "text-blue-600",
            },
            {
                label: "Products",
                value: medStore.products?.length || 0,
                icon: Package,
                bgColor: "bg-purple-100",
                iconColor: "text-purple-600",
            },
            {
                label: "Notifications",
                value: notificationCount.value,
                icon: Bell,
                bgColor: "bg-orange-100",
                iconColor: "text-orange-600",
            },
        ];
    });
    // Methods
    const handleNavigation = (tabKey) => {
        activeTab.value = tabKey;
        sidebarOpen.value = false;
        router.push({ query: { tab: tabKey } });
    };

    const handleLogout = () => {
        authStore.logout();
        router.push("/");
    };

    // Watch for tab changes
    watch(
        () => route.query.tab,
        (newTab) => {
            if (newTab) activeTab.value = newTab;
        }
    );

    // Lifecycle
    onMounted(() => {
        // Fetch initial data
        orderStore.fetchAllOrders();
        medStore.fetchProducts();
        notificationStore.fetchNotifications();
        notificationStore.startPolling();
    });

    onUnmounted(() => {
        notificationStore.stopPolling();
    });
</script>
<template>
    <BaseLayout
        :title="pageTitle"
        :sidebar-open="sidebarOpen"
        :notification-count="notificationCount"
        :user-name="userName"
        :user-role="userRole"
        :show-search="activeTab === 'medication'"
        @toggle-sidebar="sidebarOpen = !sidebarOpen"
        @logout="handleLogout"
    >
        <template #navigation>
            <NavigationMenu
                :navigation="navigationItems"
                :active-tab="activeTab"
                @navigate="handleNavigation"
            />
        </template>

        <!-- Main Content -->
        <div class="p-4 sm:p-6">
            <!-- Overview -->
            <StatsGrid v-if="activeTab === 'overview'" :stats="overviewStats" />
            <!-- Recent Activity -->

            <!-- Medications -->
            <MedicationManager
                v-else-if="activeTab === 'medication'"
                :user-role="userRole"
            />

            <!-- Orders -->
            <OrderManager
                v-else-if="activeTab === 'orders'"
                :user-role="userRole"
            />

            <!-- Sales -->
            <SalesManager
                v-else-if="activeTab === 'sales'"
                :user-role="userRole"
            />

            <!-- Staff (Admin only) -->
            <StaffManager
                v-else-if="activeTab === 'staff' && userRole === 'admin'"
            />

            <!-- Notifications -->
            <NotificationManager v-else-if="activeTab === 'notifications'" />
        </div>
    </BaseLayout>
</template>
