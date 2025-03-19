<script setup>
    defineProps({
        labelname: {
            type: String,
            required: true,
            default: "Signup",
        },
        type: {
            type: String,
            default: "text",
        },
        modelName: {
            type: String,
            default: "",
        },
    });
</script>

<template>
    <label class="block mx-auto mt-3 text-sm text-gray-900">
        {{ labelname }}
        <input
            :type="type"
            :value="modelName"
            @input="$emit('update:modelname', $event.target.value)"
            required
            autocomplete="on"
            class="block mt-1 w-full mx-auto border border-gray-400 rounded outline-none focus:border-orange-700 h-9 p-1 md:h-10 bg-transparent"
        />
    </label>
</template>
