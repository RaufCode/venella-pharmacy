<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <!-- Mobile Header -->
    <header
      class="lg:hidden fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200"
    >
      <div class="px-4 py-3 flex items-center justify-between">
        <button
          @click="$emit('toggle-sidebar')"
          class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <Menu class="w-5 h-5 text-gray-600" />
        </button>

        <h1 class="text-lg font-semibold text-gray-800 truncate">
          {{ title }}
        </h1>

        <div class="flex items-center gap-2">
          <!-- Notifications -->
          <button
            class="relative p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <Bell class="w-5 h-5 text-gray-600" />
            <span
              v-if="notificationCount > 0"
              class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center"
            >
              {{ notificationCount > 9 ? "9+" : notificationCount }}
            </span>
          </button>

          <!-- User Menu -->
          <div class="relative">
            <button
              @click="showUserMenu = !showUserMenu"
              class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <User class="w-5 h-5 text-gray-600" />
            </button>

            <!-- Dropdown -->
            <div
              v-if="showUserMenu"
              class="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2"
            >
              <div class="px-4 py-2 border-b border-gray-100">
                <p class="text-sm font-medium text-gray-900">{{ userName }}</p>
                <p class="text-xs text-gray-500">{{ userRole }}</p>
              </div>

              <button
                @click="$emit('logout')"
                class="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 transition-colors"
              >
                <LogOut class="w-4 h-4 inline mr-2" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="flex h-screen pt-16 lg:pt-0">
      <!-- Sidebar -->
      <aside
        :class="[
          'fixed lg:static inset-y-0 left-0 z-40 w-72 bg-white border-r border-gray-200 transform transition-transform duration-300 lg:translate-x-0',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full',
        ]"
      >
        <div class="flex flex-col h-full">
          <!-- Logo -->
          <div class="px-6 py-6 border-b border-gray-200">
            <div class="flex items-center gap-3">
              <div
                class="w-10 h-10 bg-gradient-to-br from-orange-500 to-red-600 rounded-xl flex items-center justify-center"
              >
                <Pill class="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 class="text-xl font-bold text-gray-900">VPharm</h1>
                <p class="text-xs text-gray-500">Venella Pharmacy</p>
              </div>
            </div>
          </div>

          <!-- Navigation -->
          <nav class="flex-1 px-4 py-6 space-y-2">
            <slot name="navigation" />
          </nav>

          <!-- User Section (Desktop) -->
          <div class="hidden lg:block px-4 py-6 border-t border-gray-200">
            <div class="flex items-center gap-3 mb-4">
              <div
                class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center"
              >
                <span class="text-white font-semibold text-sm">
                  {{ userName?.charAt(0)?.toUpperCase() }}
                </span>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 truncate">
                  {{ userName }}
                </p>
                <p class="text-xs text-gray-500">{{ userRole }}</p>
              </div>
            </div>

            <button
              @click="$emit('logout')"
              class="w-full flex items-center gap-2 px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            >
              <LogOut class="w-4 h-4" />
              Logout
            </button>
          </div>
        </div>
      </aside>

      <!-- Overlay for mobile -->
      <div
        v-if="sidebarOpen"
        @click="$emit('toggle-sidebar')"
        class="lg:hidden fixed inset-0 z-30 bg-gray-900/50 backdrop-blur-sm"
      ></div>

      <!-- Main Content -->
      <main class="flex-1 flex flex-col min-w-0">
        <!-- Desktop Header -->
        <header
          class="hidden lg:flex items-center justify-between px-8 py-6 bg-white border-b border-gray-200"
        >
          <div>
            <h1 class="text-2xl font-bold text-gray-900">{{ title }}</h1>
            <p class="text-sm text-gray-500 mt-1">{{ subtitle }}</p>
          </div>

          <div class="flex items-center gap-4">
            <!-- Search (if needed) -->
            <div v-if="showSearch" class="relative">
              <Search
                class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400"
              />
              <input
                type="text"
                placeholder="Search..."
                class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              />
            </div>

            <!-- Notifications -->
            <button
              class="relative p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <Bell class="w-5 h-5 text-gray-600" />
              <span
                v-if="notificationCount > 0"
                class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center"
              >
                {{ notificationCount > 9 ? "9+" : notificationCount }}
              </span>
            </button>
          </div>
        </header>

        <!-- Page Content -->
        <div class="flex-1 overflow-auto">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import { Menu, Bell, User, LogOut, Pill, Search } from "lucide-vue-next";

  defineProps({
    title: {
      type: String,
      default: "Dashboard",
    },
    subtitle: {
      type: String,
      default: "",
    },
    sidebarOpen: {
      type: Boolean,
      default: false,
    },
    notificationCount: {
      type: Number,
      default: 0,
    },
    userName: {
      type: String,
      default: "User",
    },
    userRole: {
      type: String,
      default: "User",
    },
    showSearch: {
      type: Boolean,
      default: false,
    },
  });

  defineEmits(["toggle-sidebar", "logout"]);

  const showUserMenu = ref(false);
</script>
