<script setup>
    import { computed } from "vue";

    const props = defineProps({
        modelValue: {
            type: [String, Number],
            default: "",
        },
        type: {
            type: String,
            default: "text",
        },
        label: {
            type: String,
            default: "",
        },
        placeholder: {
            type: String,
            default: "",
        },
        id: {
            type: String,
            default: () => `input-${Math.random().toString(36).substr(2, 9)}`,
        },
        size: {
            type: String,
            default: "md",
            validator: (value) => ["sm", "md", "lg"].includes(value),
        },
        disabled: {
            type: Boolean,
            default: false,
        },
        readonly: {
            type: Boolean,
            default: false,
        },
        required: {
            type: Boolean,
            default: false,
        },
        errorMessage: {
            type: String,
            default: "",
        },
        successMessage: {
            type: String,
            default: "",
        },
        helpText: {
            type: String,
            default: "",
        },
    });

    const emit = defineEmits(["update:modelValue"]);

    const localValue = computed({
        get() {
            return props.modelValue;
        },
        set(value) {
            emit("update:modelValue", value);
        },
    });

    const sizeClasses = computed(() => {
        const sizes = {
            sm: "py-1.5 text-sm",
            md: "py-2 text-sm",
            lg: "py-3 text-base",
        };
        return sizes[props.size];
    });
</script>

<template>
    <div class="relative">
        <label
            v-if="label"
            :for="id"
            class="block text-sm font-medium text-gray-700 mb-2"
        >
            {{ label }}
            <span v-if="required" class="text-red-500 ml-1">*</span>
        </label>

        <div class="relative">
            <div
                v-if="$slots.icon"
                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
            >
                <slot name="icon" />
            </div>

            <input
                :id="id"
                v-model="localValue"
                v-bind="$attrs"
                :type="type"
                :placeholder="placeholder"
                :disabled="disabled"
                :readonly="readonly"
                :class="[
                    'block w-full border border-gray-300 rounded-lg shadow-sm transition-all duration-200 focus:ring-2 focus:ring-orange-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed',
                    sizeClasses,
                    $slots.icon ? 'pl-10' : 'pl-3',
                    errorMessage ? 'border-red-300 focus:ring-red-500' : '',
                    successMessage
                        ? 'border-green-300 focus:ring-green-500'
                        : '',
                ]"
            />

            <div
                v-if="$slots.suffix"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
            >
                <slot name="suffix" />
            </div>
        </div>

        <div
            v-if="helpText && !errorMessage && !successMessage"
            class="mt-1 text-sm text-gray-500"
        >
            {{ helpText }}
        </div>

        <div v-if="errorMessage" class="mt-1 text-sm text-red-600">
            {{ errorMessage }}
        </div>

        <div v-if="successMessage" class="mt-1 text-sm text-green-600">
            {{ successMessage }}
        </div>
    </div>
</template>
