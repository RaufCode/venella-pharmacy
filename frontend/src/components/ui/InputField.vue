<script setup>
    defineEmits(["update:modelValue"]);
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
        modelValue: {
            type: [String, Number],
            default: "",
        },
        name: {
            type: String,
            required: false,
        },
        autocomplete: {
            type: String,
            required: false,
        },
    });
</script>

<template>
    <label class="block mx-auto mt-3 text-sm text-gray-900">
        {{ labelname }}
        <input
            :type="type"
            :value="modelValue"
            :name="name"
            :autocomplete="autocomplete"
            @input="$emit('update:modelValue', $event.target.value)"
            required
            class="block mt-1 w-full mx-auto border border-gray-400 rounded outline-none focus:border-orange-700 h-9 px-4 md:h-10 bg-transparent"
        />
    </label>
</template>
