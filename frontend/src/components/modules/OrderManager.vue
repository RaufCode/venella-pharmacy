<template>
  <div class="space-y-6">
    <!-- Header with Filters -->
    <div
      class="flex flex-col lg:flex-row lg:items-center justify-between gap-4"
    >
      <div>
        <h2 class="text-xl font-semibold text-gray-900">Order Management</h2>
        <p class="text-sm text-gray-600">Track and manage customer orders</p>
      </div>

      <div class="flex flex-col sm:flex-row items-start sm:items-center gap-3">
        <BaseInput
          v-model="searchTerm"
          placeholder="Search orders..."
          size="sm"
          class="w-full sm:w-64"
        >
          <template #icon>
            <Search class="w-4 h-4 text-gray-400" />
          </template>
        </BaseInput>

        <BaseInput
          type="date"
          v-model="selectedDate"
          size="sm"
          class="w-full sm:w-auto"
        />
      </div>
    </div>

    <!-- Order Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-4 gap-4">
      <div
        v-for="stat in orderStats"
        :key="stat.label"
        class="bg-white rounded-lg border border-gray-200 p-4"
      >
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600">{{ stat.label }}</p>
            <p class="text-xl font-semibold text-gray-900 mt-1">
              {{ stat.value }}
            </p>
          </div>
          <div
            :class="[
              'w-10 h-10 rounded-lg flex items-center justify-center',
              stat.bgColor,
            ]"
          >
            <component :is="stat.icon" :class="['w-5 h-5', stat.iconColor]" />
          </div>
        </div>
      </div>
    </div>

    <!-- Order Filters -->
    <BaseCard>
      <template #header>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="filter in orderFilters"
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
              class="ml-2 text-xs opacity-75"
            >
              {{ filter.count }}
            </span>
          </button>
        </div>
      </template>

      <!-- Orders Table/List -->
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div
          class="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"
        ></div>
      </div>

      <div v-else-if="filteredOrders.length === 0" class="text-center py-12">
        <ShoppingCart class="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-900">No orders found</h3>
        <p class="text-gray-500">No orders match your current filters.</p>
      </div>

      <div v-else>
        <!-- Desktop Table -->
        <div class="hidden lg:block overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Order
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Customer
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Date
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Status
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Total
                </th>
                <th
                  class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="order in paginatedOrders"
                :key="order.id"
                class="hover:bg-gray-50 transition-colors cursor-pointer"
                @click="viewOrder(order)"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">
                    #{{ order.id }}
                  </div>
                  <div class="text-sm text-gray-500">
                    {{ order.order_items?.length || 0 }} items
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">
                    {{ order.customer_name }}
                  </div>
                  <div class="text-sm text-gray-500">
                    {{ order.customer_phone }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">
                    {{ formatDate(order.created_at) }}
                  </div>
                  <div class="text-sm text-gray-500">
                    {{ formatTime(order.created_at) }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getStatusClasses(order.status)">
                    {{ order.status }}
                  </span>
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                >
                  ₵{{ parseFloat(order.total_amount || 0).toFixed(2) }}
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
                  @click.stop
                >
                  <div class="flex items-center justify-end gap-2">
                    <BaseButton
                      v-if="order.status === 'pending'"
                      size="sm"
                      variant="secondary"
                      @click="updateOrderStatus(order.id, 'processing')"
                    >
                      Process
                    </BaseButton>
                    <BaseButton
                      v-if="order.status === 'processing'"
                      size="sm"
                      variant="success"
                      @click="updateOrderStatus(order.id, 'delivered')"
                    >
                      Mark Delivered
                    </BaseButton>
                    <button
                      @click="viewOrder(order)"
                      class="text-orange-600 hover:text-orange-700 p-1 rounded"
                    >
                      <Eye class="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Mobile Card View -->
        <div class="lg:hidden space-y-4">
          <div
            v-for="order in paginatedOrders"
            :key="order.id"
            class="bg-white border border-gray-200 rounded-lg p-4 shadow-sm cursor-pointer hover:shadow-md transition-shadow"
            @click="viewOrder(order)"
          >
            <div class="flex items-start justify-between mb-3">
              <div>
                <h3 class="text-sm font-medium text-gray-900">
                  #{{ order.id }}
                </h3>
                <p class="text-xs text-gray-500 mt-1">
                  {{ order.order_items?.length || 0 }} items
                </p>
              </div>
              <span :class="getStatusClasses(order.status)">
                {{ order.status }}
              </span>
            </div>

            <div class="space-y-2 text-sm">
              <div class="flex items-center justify-between">
                <span class="text-gray-600">Customer:</span>
                <span class="font-medium">{{ order.customer_name }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-600">Date:</span>
                <span>{{ formatDate(order.created_at) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-gray-600">Total:</span>
                <span class="font-semibold"
                  >₵{{ parseFloat(order.total_amount || 0).toFixed(2) }}</span
                >
              </div>
            </div>

            <div class="flex items-center gap-2 mt-4" @click.stop>
              <BaseButton
                v-if="order.status === 'pending'"
                size="sm"
                variant="secondary"
                @click="updateOrderStatus(order.id, 'processing')"
                class="flex-1"
              >
                Process Order
              </BaseButton>
              <BaseButton
                v-if="order.status === 'processing'"
                size="sm"
                variant="success"
                @click="updateOrderStatus(order.id, 'delivered')"
                class="flex-1"
              >
                Mark Delivered
              </BaseButton>
              <button
                @click="viewOrder(order)"
                class="p-2 text-orange-600 hover:text-orange-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <Eye class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div
          v-if="totalPages > 1"
          class="flex items-center justify-between mt-6"
        >
          <div class="text-sm text-gray-500">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to
            {{ Math.min(currentPage * itemsPerPage, filteredOrders.length) }} of
            {{ filteredOrders.length }} orders
          </div>

          <div class="flex items-center gap-2">
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

<script setup>
  import { ref, computed, onMounted } from "vue";
  import { useRouter } from "vue-router";
  import {
    Search,
    ShoppingCart,
    Eye,
    ChevronLeft,
    ChevronRight,
    Clock,
    CheckCircle,
    Package,
    AlertCircle,
  } from "lucide-vue-next";

  import BaseCard from "@/components/shared/BaseCard.vue";
  import BaseButton from "@/components/shared/BaseButton.vue";
  import BaseInput from "@/components/shared/BaseInput.vue";

  import { useOrderStore } from "@/stores/orderStore";

  const props = defineProps({
    userRole: {
      type: String,
      required: true,
    },
  });

  const router = useRouter();
  const orderStore = useOrderStore();

  const searchTerm = ref("");
  const selectedDate = ref("");
  const activeFilter = ref("all");
  const currentPage = ref(1);
  const itemsPerPage = 10;

  const isLoading = computed(() => orderStore.loading);
  const orders = computed(() => orderStore.orders || []);

  const orderFilters = computed(() => [
    { key: "all", label: "All Orders", count: orders.value.length },
    {
      key: "pending",
      label: "Pending",
      count: orders.value.filter((o) => o.status?.toLowerCase() === "pending")
        .length,
    },
    {
      key: "processing",
      label: "Processing",
      count: orders.value.filter(
        (o) => o.status?.toLowerCase() === "processing"
      ).length,
    },
    {
      key: "delivered",
      label: "Delivered",
      count: orders.value.filter((o) => o.status?.toLowerCase() === "delivered")
        .length,
    },
  ]);

  const orderStats = computed(() => [
    {
      label: "Total Orders",
      value: orders.value.length,
      icon: ShoppingCart,
      bgColor: "bg-blue-100",
      iconColor: "text-blue-600",
    },
    {
      label: "Pending",
      value: orders.value.filter((o) => o.status?.toLowerCase() === "pending")
        .length,
      icon: Clock,
      bgColor: "bg-yellow-100",
      iconColor: "text-yellow-600",
    },
    {
      label: "Processing",
      value: orders.value.filter(
        (o) => o.status?.toLowerCase() === "processing"
      ).length,
      icon: Package,
      bgColor: "bg-orange-100",
      iconColor: "text-orange-600",
    },
    {
      label: "Delivered",
      value: orders.value.filter((o) => o.status?.toLowerCase() === "delivered")
        .length,
      icon: CheckCircle,
      bgColor: "bg-green-100",
      iconColor: "text-green-600",
    },
  ]);

  const filteredOrders = computed(() => {
    let filtered = [...orders.value];

    // Filter by status
    if (activeFilter.value !== "all") {
      filtered = filtered.filter(
        (order) => order.status?.toLowerCase() === activeFilter.value
      );
    }

    // Filter by search term
    if (searchTerm.value) {
      const term = searchTerm.value.toLowerCase();
      filtered = filtered.filter(
        (order) =>
          order.id.toString().includes(term) ||
          order.customer_name?.toLowerCase().includes(term) ||
          order.customer_phone?.includes(term)
      );
    }

    // Filter by date
    if (selectedDate.value) {
      filtered = filtered.filter((order) => {
        const orderDate = new Date(order.created_at)
          .toISOString()
          .split("T")[0];
        return orderDate === selectedDate.value;
      });
    }

    return filtered.sort(
      (a, b) => new Date(b.created_at) - new Date(a.created_at)
    );
  });

  const totalPages = computed(() =>
    Math.ceil(filteredOrders.value.length / itemsPerPage)
  );

  const paginatedOrders = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return filteredOrders.value.slice(start, end);
  });

  const getStatusClasses = (status) => {
    const baseClasses = "px-2 py-1 text-xs font-medium rounded-full";
    switch (status?.toLowerCase()) {
      case "pending":
        return `${baseClasses} bg-yellow-100 text-yellow-800`;
      case "processing":
        return `${baseClasses} bg-orange-100 text-orange-800`;
      case "delivered":
        return `${baseClasses} bg-green-100 text-green-800`;
      case "cancelled":
        return `${baseClasses} bg-red-100 text-red-800`;
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`;
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const formatTime = (dateString) => {
    return new Date(dateString).toLocaleTimeString();
  };

  const updateOrderStatus = async (orderId, status) => {
    try {
      await orderStore.updateOrderStatus(orderId, status);
      await orderStore.fetchAllOrders();
    } catch (error) {
      console.error("Failed to update order status:", error);
    }
  };

  const viewOrder = (order) => {
    router.push(`/order/${order.id}`);
  };

  onMounted(() => {
    orderStore.fetchAllOrders();
  });
</script>
