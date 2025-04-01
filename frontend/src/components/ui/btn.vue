<script setup>
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
        class="bg-orange-700 font-medium mt-4 block mx-auto w-full h-9 rounded text-white border border-orange-700 hover:bg-orange-600 md:h-10"
    >
        {{ btnName }}
    </button>
</template>
