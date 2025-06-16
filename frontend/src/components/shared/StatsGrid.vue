<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Stats Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div
        v-for="stat in stats"
        :key="stat.label"
        class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
      >
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600">{{ stat.label }}</p>
            <p class="text-2xl font-bold text-gray-900 mt-1">
              {{ stat.value }}
            </p>
            <div
              v-if="stat.change"
              :class="[
                'text-xs font-medium mt-1',
                stat.changeType === 'increase'
                  ? 'text-green-600'
                  : 'text-red-600',
              ]"
            >
              {{ stat.changeType === "increase" ? "↗" : "↘" }} {{ stat.change }}
            </div>
          </div>
          <div
            :class="[
              'w-12 h-12 rounded-lg flex items-center justify-center',
              stat.bgColor,
            ]"
          >
            <component :is="stat.icon" :class="['w-6 h-6', stat.iconColor]" />
          </div>
        </div>
      </div>
    </div>

    <!-- Additional Content -->
    <div class="space-y-6">
      <slot />
    </div>
  </div>
</template>

<script setup>
  defineProps({
    stats: {
      type: Array,
      required: true,
    },
  });
</script>
