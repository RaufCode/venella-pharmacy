<template>
  <button
    v-bind="$attrs"
    :disabled="disabled || loading"
    :class="[
      'inline-flex items-center justify-center font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed',
      sizeClasses,
      variantClasses,
      roundedClasses,
      { 'cursor-not-allowed': disabled || loading },
    ]"
  >
    <div v-if="loading" class="flex items-center gap-2">
      <div
        class="w-4 h-4 border-2 border-current border-t-transparent animate-spin rounded-full"
      ></div>
      <span v-if="$slots.default">Loading...</span>
    </div>

    <div v-else class="flex items-center gap-2">
      <slot name="icon" />
      <slot />
    </div>
  </button>
</template>

<script setup>
  import { computed } from "vue";

  const props = defineProps({
    variant: {
      type: String,
      default: "primary",
      validator: (value) =>
        [
          "primary",
          "secondary",
          "danger",
          "success",
          "ghost",
          "outline",
        ].includes(value),
    },
    size: {
      type: String,
      default: "md",
      validator: (value) => ["xs", "sm", "md", "lg", "xl"].includes(value),
    },
    rounded: {
      type: String,
      default: "lg",
      validator: (value) =>
        ["none", "sm", "md", "lg", "xl", "full"].includes(value),
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  });

  const sizeClasses = computed(() => {
    const sizes = {
      xs: "px-2 py-1 text-xs",
      sm: "px-3 py-1.5 text-sm",
      md: "px-4 py-2 text-sm",
      lg: "px-6 py-2.5 text-base",
      xl: "px-8 py-3 text-lg",
    };
    return sizes[props.size];
  });

  const variantClasses = computed(() => {
    const variants = {
      primary:
        "bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 text-white focus:ring-orange-500 shadow-lg hover:shadow-xl",
      secondary:
        "bg-gray-100 hover:bg-gray-200 text-gray-900 focus:ring-gray-500",
      danger:
        "bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white focus:ring-red-500 shadow-lg hover:shadow-xl",
      success:
        "bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white focus:ring-green-500 shadow-lg hover:shadow-xl",
      ghost:
        "bg-transparent hover:bg-gray-100 text-gray-700 focus:ring-gray-500",
      outline:
        "border border-gray-300 bg-white hover:bg-gray-50 text-gray-700 focus:ring-gray-500",
    };
    return variants[props.variant];
  });

  const roundedClasses = computed(() => {
    const rounded = {
      none: "rounded-none",
      sm: "rounded-sm",
      md: "rounded-md",
      lg: "rounded-lg",
      xl: "rounded-xl",
      full: "rounded-full",
    };
    return rounded[props.rounded];
  });
</script>
