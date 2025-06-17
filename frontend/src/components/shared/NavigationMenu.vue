<script setup>
    const props = defineProps({
        navigation: {
            type: Array,
            required: true,
        },
        activeTab: {
            type: String,
            required: true,
        },
    });

    defineEmits(["navigate"]);

    const isActive = (key) => {
        return props.activeTab === key;
    };
</script>
<template>
    <nav class="space-y-1">
        <template v-for="item in navigation" :key="item.key">
            <button
                @click="$emit('navigate', item.key)"
                :class="[
                    'w-full flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg transition-all duration-200 group',
                    isActive(item.key)
                        ? 'bg-gradient-to-r from-orange-500 to-red-600 text-white shadow-lg'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100',
                ]"
            >
                <component
                    :is="item.icon"
                    :class="[
                        'w-5 h-5 transition-colors',
                        isActive(item.key)
                            ? 'text-white'
                            : 'text-gray-400 group-hover:text-gray-600',
                    ]"
                />
                <span>{{ item.label }}</span>

                <!-- Badge for notifications -->
                <span
                    v-if="item.badge && item.badge > 0"
                    :class="[
                        'ml-auto px-2 py-0.5 text-xs font-semibold rounded-full',
                        isActive(item.key)
                            ? 'bg-white/20 text-white'
                            : 'bg-red-100 text-red-600',
                    ]"
                >
                    {{ item.badge > 99 ? "99+" : item.badge }}
                </span>
            </button>
        </template>
    </nav>
</template>
