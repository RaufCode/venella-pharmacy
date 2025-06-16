<template>
  <BaseLayout
    :title="pageTitle"
    :subtitle="pageSubtitle"
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
    <div class="p-6">
      <!-- Overview -->
      <StatsGrid v-if="activeTab === 'overview'" :stats="overviewStats">
        <!-- Recent Activity -->
        <BaseCard
          title="Recent Activity"
          subtitle="Latest updates from your pharmacy"
        >
          <div class="space-y-4">
            <div
              v-for="activity in recentActivities"
              :key="activity.id"
              class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg"
            >
              <div
                :class="[
                  'w-10 h-10 rounded-full flex items-center justify-center',
                  activity.bgColor,
                ]"
              >
                <component
                  :is="activity.icon"
                  :class="['w-5 h-5', activity.iconColor]"
                />
              </div>
              <div class="flex-1">
                <p class="text-sm font-medium text-gray-900">
                  {{ activity.title }}
                </p>
                <p class="text-xs text-gray-600">{{ activity.description }}</p>
                <p class="text-xs text-gray-500 mt-1">
                  {{ formatTime(activity.time) }}
                </p>
              </div>
            </div>
          </div>
        </BaseCard>
      </StatsGrid>

      <!-- Medications -->
      <MedicationManager
        v-else-if="activeTab === 'medication'"
        :user-role="userRole"
      />

      <!-- Orders -->
      <OrderManager v-else-if="activeTab === 'orders'" :user-role="userRole" />

      <!-- Sales -->
      <SalesManager v-else-if="activeTab === 'sales'" :user-role="userRole" />

      <!-- Staff (Admin only) -->
      <StaffManager v-else-if="activeTab === 'staff' && userRole === 'admin'" />

      <!-- Notifications -->
      <NotificationManager v-else-if="activeTab === 'notifications'" />
    </div>
  </BaseLayout>
</template>

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
  import BaseCard from "@/components/shared/BaseCard.vue";
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
      overview: "Dashboard Overview",
      medication: "Medication Management",
      orders: "Order Management",
      sales: "Sales Analytics",
      staff: "Staff Management",
      notifications: "Notifications",
    };
    return titles[activeTab.value] || "Dashboard";
  });

  const pageSubtitle = computed(() => {
    const subtitles = {
      overview: `Welcome back, ${userName.value}!`,
      medication: "Manage your pharmacy inventory",
      orders: "Track and process customer orders",
      sales: "Monitor your sales performance",
      staff: "Manage staff members and permissions",
      notifications: "Stay updated with latest alerts",
    };
    return subtitles[activeTab.value] || "";
  });

  // Notification count
  const notificationCount = computed(() => notificationStore.unreadCount || 0);

  // Overview stats
  const overviewStats = computed(() => {
    return [
      {
        label: "Total Sales",
        value: `₵${orderStore.totalSales || "0.00"}`,
        change: "+12%",
        changeType: "increase",
        icon: TrendingUp,
        bgColor: "bg-green-100",
        iconColor: "text-green-600",
      },
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

  // Recent activities (mock data for now)
  const recentActivities = ref([
    {
      id: 1,
      title: "New order received",
      description: "Order #1234 has been placed",
      time: new Date(),
      icon: ShoppingCart,
      bgColor: "bg-blue-100",
      iconColor: "text-blue-600",
    },
    {
      id: 2,
      title: "Low stock alert",
      description: "Paracetamol is running low",
      time: new Date(Date.now() - 30 * 60 * 1000),
      icon: AlertCircle,
      bgColor: "bg-red-100",
      iconColor: "text-red-600",
    },
    {
      id: 3,
      title: "Order completed",
      description: "Order #1230 has been delivered",
      time: new Date(Date.now() - 60 * 60 * 1000),
      icon: CheckCircle,
      bgColor: "bg-green-100",
      iconColor: "text-green-600",
    },
  ]);

  // Methods
  const handleNavigation = (tabKey) => {
    activeTab.value = tabKey;
    sidebarOpen.value = false;
    router.push({ query: { tab: tabKey } });
  };

  const handleLogout = () => {
    authStore.logout();
    router.push("/login");
  };

  const formatTime = (time) => {
    const now = new Date();
    const diff = now - time;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);

    if (minutes < 1) return "Just now";
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return time.toLocaleDateString();
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
