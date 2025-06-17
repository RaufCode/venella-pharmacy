<script setup>
    defineProps({
        stats: {
            type: Array,
            required: true,
        },
    });
</script>

<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Stats Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <div
                v-for="stat in stats"
                :key="stat.label"
                class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
            >
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm font-medium text-gray-600">
                            {{ stat.label }}
                        </p>
                        <p class="text-2xl font-bold text-gray-900 mt-1">
                            {{ stat.value }}
                        </p>
                    </div>
                    <div
                        :class="[
                            'w-12 h-12 rounded-lg flex items-center justify-center',
                            stat.bgColor,
                        ]"
                    >
                        <component
                            :is="stat.icon"
                            :class="['w-6 h-6', stat.iconColor]"
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
