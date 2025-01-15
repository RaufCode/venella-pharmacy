<script setup>
    import { defineProps } from "vue";
    defineProps({
        btnName: {
            type: String,
            required: true,
            default: "button",
        },
    });
</script>
<template>
    <button
        type="submit"
        class="bg-orange-700 font-medium mt-4 block mx-auto w-full h-8 rounded text-white border border-orange-700 hover:bg-orange-600"
    >
        {{ btnName }}
    </button>
</template>
