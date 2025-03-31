<script setup>
    import { ref } from "vue";
    import btn from "@/components/ui/Btn.vue";
    import InputField from "@/components/ui/InputField.vue";

    const addModal = ref(false);
</script>

<template>
    <div class="w-full px-3">
        <div class="pt-2 md:pt-5">
            <h1 class="text-lg font-poppins font-semibold text-blue-600">
                Medications
            </h1>
            <p class="tracking-widest text-sm mb-3">
                Easily browse, search, and manage all available medications
            </p>
        </div>
        <div
            class="flex justify-start gap-2 items-center text-sm w-full max-w-[500px] relative"
        >
            <!-- <label class="w-4/5">
                <input
                    type="search"
                    placeholder="Search for medicine"
                    class="border border-gray-400 rounded outline-none w-full focus:border-orange-700 h-10 pl-5"
                />
            </label>
            <button
                class="bg-orange-600 h-10 text-white rounded px-2 hover:bg-orange-500 shadow-md transition-all duration-500"
            >
                Search
            </button> -->
            <div
                class="hidden w-full absolute top-11 bg-gray-50 shadow p-2 z-20"
            >
                <h1>Medication List</h1>
            </div>
        </div>
        <div class="">
            <button
                @click="addModal = true"
                class="bg-blue-600 h-10 w-32 block text-white text-sm px-2 hover:bg-blue-500 shadow-md transition-all duration-500 md:w-36"
            >
                Add Medication
            </button>
        </div>
    </div>
    <!--Add Medication Modal-->
    <div
        v-if="addModal"
        class="bg-black bg-opacity-50 inset-0 w-full h-screen flex items-center justify-center fixed top-0 left-0 z-50 max-w-[1440px]"
    >
        <form class="bg-white rounded-lg shadow-lg w-11/12 max-w-md p-4">
            <div class="flex justify-between items-center border-b-2 pb-2">
                <h2 class="form-title text-lg font-semibold">Add Medication</h2>
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

    <template />
</template>
