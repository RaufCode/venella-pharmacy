<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200">
    <!-- Header -->
    <div
      v-if="title || $slots.header"
      class="px-6 py-4 border-b border-gray-200"
    >
      <div class="flex items-center justify-between">
        <div>
          <h3 v-if="title" class="text-lg font-semibold text-gray-900">
            {{ title }}
          </h3>
          <p v-if="subtitle" class="text-sm text-gray-600 mt-1">
            {{ subtitle }}
          </p>
        </div>
        <slot name="header" />
      </div>
    </div>

    <!-- Filters/Tabs -->
    <div v-if="tabs.length > 0" class="px-6 py-3 border-b border-gray-200">
      <div class="flex flex-wrap gap-2">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="$emit('tab-change', tab.key)"
          :class="[
            'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
            tab.key === activeTab
              ? 'bg-orange-100 text-orange-700 border border-orange-200'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100',
          ]"
        >
          {{ tab.label }}
          <span v-if="tab.count !== undefined" class="ml-2 text-xs opacity-75">
            {{ tab.count }}
          </span>
        </button>
      </div>
    </div>

    <!-- Content -->
    <div class="p-6">
      <slot />
    </div>

    <!-- Footer -->
    <div v-if="$slots.footer" class="px-6 py-4 border-t border-gray-200">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
  defineProps({
    title: {
      type: String,
      default: "",
    },
    subtitle: {
      type: String,
      default: "",
    },
    tabs: {
      type: Array,
      default: () => [],
    },
    activeTab: {
      type: String,
      default: "",
    },
  });

  defineEmits(["tab-change"]);
</script>
