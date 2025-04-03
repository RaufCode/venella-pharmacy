<script setup>
    import { ref } from "vue";
    import btn from "@/components/ui/Btn.vue";
    import InputField from "@/components/ui/InputField.vue";

    const addModal = ref(false);
</script>

<template>
    <div class="h-screen overflow-y-scroll">
        <div
            class="mt-2 px-3 py-3 md:bg-white flex justify-between items-center shadow md:mt-0 md:py-5 md:px-5"
        >
            <h1 class="text-xl font-styleScript text-orange-600 md:text-3xl">
                Medications
            </h1>
            <button
                @click="addModal = true"
                class="bg-green-700 block text-white text-sm px-4 py-2 rounded hover:bg-green-600 shadow-md transition-all duration-500"
            >
                Add Med
            </button>
        </div>
        <!--Add Medication Modal-->
        <div
            v-if="addModal"
            class="bg-black bg-opacity-50 inset-0 w-full h-screen flex items-center justify-center fixed top-0 left-0 z-50 max-w-[1440px]"
        >
            <form class="bg-white rounded-lg shadow-lg w-11/12 max-w-md p-4">
                <div class="flex justify-between items-center border-b-2 pb-2">
                    <h2 class="form-title text-lg font-semibold">
                        Add Medication
                    </h2>
                    <button @click="addModal = false" class="block">
                        <i class="pi pi-times text-blue-500"></i>
                    </button>
                </div>
                <InputField labelname="Name" type="text" />
                <InputField labelname="Dosage" type="text" />
                <label class="block mx-auto mt-3 text-sm text-gray-900">
                    Category
                    <select
                        class="block mt-1 w-full mx-auto border border-gray-400 rounded outline-none focus:border-orange-700 h-9 p-1 md:h-10"
                        required
                    >
                        <option disabled value="">Select Category</option>
                    </select>
                </label>
                <label class="block mx-auto mt-3 text-sm text-gray-900">
                    Type
                    <select
                        class="block mt-1 w-full mx-auto border border-gray-400 rounded outline-none focus:border-orange-700 h-9 p-1 md:h-10"
                        required
                    >
                        <option disabled value="">Select Type</option>
                    </select>
                </label>
                <label class="block mx-auto mt-3 text-sm text-gray-900">
                    Quantity
                    <select
                        class="block mt-1 w-full mx-auto border border-gray-400 rounded outline-none focus:border-orange-700 h-9 p-1 md:h-10"
                        required
                    >
                        <option disabled value="">Select Type</option>
                    </select>
                </label>
                <InputField labelname="Expiry Date" type="text" />
                <btn btnName="Save" />
            </form>
        </div>
    </div>

    <template />
</template>
