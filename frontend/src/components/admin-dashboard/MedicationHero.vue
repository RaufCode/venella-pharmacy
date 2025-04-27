<script setup>
    import { ref } from "vue";
    import InputField from "@/components/ui/InputField.vue";
    import Btn from "@/components/ui/Btn.vue";

    const medications = [
        {
            id: 1,
            name: "Paracetamol",
            quantity: 120,
            category: "Pain Relief",
            type: "Tablet",
            expiryDate: "2026-02-15",
            isPrescriptionRequired: false,
        },
        {
            id: 2,
            name: "Amoxicillin",
            quantity: 80,
            category: "Antibiotic",
            type: "Capsule",
            expiryDate: "2025-10-01",
            isPrescriptionRequired: true,
        },
        {
            id: 3,
            name: "Cetirizine",
            quantity: 200,
            category: "Allergy",
            type: "Tablet",
            expiryDate: "2026-06-30",
            isPrescriptionRequired: false,
        },
        {
            id: 4,
            name: "Ibuprofen",
            quantity: 150,
            category: "Pain Relief",
            type: "Tablet",
            expiryDate: "2025-08-20",
            isPrescriptionRequired: false,
        },
        {
            id: 5,
            name: "Metformin",
            quantity: 90,
            category: "Diabetes",
            type: "Tablet",
            expiryDate: "2027-01-10",
            isPrescriptionRequired: true,
        },
        {
            id: 6,
            name: "Salbutamol",
            quantity: 50,
            category: "Asthma",
            type: "Inhaler",
            expiryDate: "2025-11-05",
            isPrescriptionRequired: true,
        },
        {
            id: 7,
            name: "Loratadine",
            quantity: 100,
            category: "Allergy",
            type: "Syrup",
            expiryDate: "2026-03-18",
            isPrescriptionRequired: false,
        },
        {
            id: 8,
            name: "Omeprazole",
            quantity: 110,
            category: "Digestive",
            type: "Capsule",
            expiryDate: "2026-09-22",
            isPrescriptionRequired: true,
        },
        {
            id: 9,
            name: "Dextromethorphan",
            quantity: 70,
            category: "Cough & Cold",
            type: "Syrup",
            expiryDate: "2025-12-31",
            isPrescriptionRequired: false,
        },
        {
            id: 10,
            name: "Hydrochlorothiazide",
            quantity: 60,
            category: "Hypertension",
            type: "Tablet",
            expiryDate: "2026-07-12",
            isPrescriptionRequired: true,
        },
    ];

    const showModal = ref(false);
</script>

<template>
    <div class="h-screen overflow-y-auto w-full">
        <div class="max-w-[1440px] mx-auto">
            <div
                class="w-full sticky top-0 z-40 bg-gray-50 shadow-md flex justify-between items-center p-3"
            >
                <h1 class="text-gray-600 text-lg font-semibold md:text-2xl">
                    Inventory Hub
                </h1>
                <button
                    @click="showModal = true"
                    type="submit"
                    class="py-2 px-4 bg-orange-600 text-sm text-white font-medium hover:bg-orange-500 md:text-base"
                >
                    Add Med
                </button>
            </div>
            <div
                class="p-3 md:w-[550px] lg:w-full h-[80vh] overflow-x-auto overscroll-contain"
            >
                <table
                    class="w-full text-sm text-left text-gray-500 dark:text-gray-400"
                >
                    <thead
                        class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
                    >
                        <tr>
                            <th class="px-6 py-3">Name</th>
                            <th class="px-6 py-3">Quantity</th>
                            <th class="px-6 py-3">Category</th>
                            <th class="px-6 py-3">Type</th>
                            <th class="px-6 py-3">ExpiryDate</th>
                            <th class="px-6 py-3">Prescription</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="medication in medications"
                            :key="medication.id"
                            class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                        >
                            <td
                                class="px-6 py-4 font-medium text-gray-900 dark:text-white"
                            >
                                {{ medication.name }}
                            </td>
                            <td class="px-6 py-4">
                                {{ medication.quantity }}
                            </td>
                            <td class="px-6 py-4">
                                {{ medication.category }}
                            </td>
                            <td class="px-6 py-4">{{ medication.type }}</td>
                            <td class="px-6 py-4">
                                {{ medication.expiryDate }}
                            </td>
                            <td class="px-6 py-4">
                                {{
                                    medication.isPrescriptionRequired
                                        ? "Yes"
                                        : "No"
                                }}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <!--Modal-->

            <div
                v-if="showModal"
                class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
            >
                <div
                    class="bg-white overflow-hidden shadow w-11/12 max-w-md max-h-[70vh] p-5 overflow-y-auto"
                >
                    <form class="w-full">
                        <div class="flex justify-between items-center">
                            <h1 class="form-title">Add meds</h1>
                            <p @click="showModal = false">
                                <i class="pi pi-times text-orange-600"></i>
                            </p>
                        </div>

                        <InputField labelname="Medicine Name" type="text" />
                        <InputField labelname="Batch Number" type="text" />
                        <InputField labelname="Quantity" type="number" />
                        <InputField labelname="Cost Price" type="number" />
                        <InputField labelname="Selling Price" type="number" />

                        <label class="block mx-auto mt-3 text-sm text-gray-900">
                            Category
                            <select
                                class="block mt-1 w-full mx-auto border border-gray-400 rounded outline-none focus:border-orange-700 h-9 p-1 md:h-10 bg-transparent"
                            >
                                <option disabled selected>
                                    Select Category
                                </option>
                                <option value="Antibiotic">Antibiotic</option>
                                <option value="Painkiller">Painkiller</option>
                                <option value="Antihistamine">
                                    Antihistamine
                                </option>
                                <option value="Supplement">Supplement</option>
                            </select>
                        </label>

                        <InputField
                            labelname="Manufacturing Date"
                            type="date"
                        />
                        <InputField labelname="Expiry Date" type="date" />

                        <label class="block mx-auto mt-3 text-sm text-gray-900">
                            Medicine Image (optional)
                            <input
                                type="file"
                                class="block mt-1 w-full mx-auto border border-gray-400 rounded outline-none focus:border-orange-700 h-9 p-1 md:h-10 bg-transparent"
                            />
                        </label>

                        <Btn btnName="Save" />
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
