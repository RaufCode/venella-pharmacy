<script setup>
    import { ref } from "vue";
    import InputField from "@/components/ui/InputField.vue";
    import Btn from "@/components/ui/Btn.vue";

    const medicines = [
        {
            medicineName: "Amoxicillin",
            batchNumber: "AMX202401",
            quantity: 100,
            costPrice: 2.5,
            sellingPrice: 5.0,
            category: "Capsule",
            antibiotic: true,
            manufacturingDate: "01/15/2024",
            expiryDate: "01/15/2026",
            image: null,
        },
        {
            medicineName: "Paracetamol",
            batchNumber: "PCM202402",
            quantity: 200,
            costPrice: 1.0,
            sellingPrice: 2.0,
            category: "Tablet",
            antibiotic: false,
            manufacturingDate: "02/10/2024",
            expiryDate: "02/10/2026",
            image: null,
        },
        {
            medicineName: "Ciprofloxacin",
            batchNumber: "CIP202403",
            quantity: 150,
            costPrice: 3.0,
            sellingPrice: 6.0,
            category: "Tablet",
            antibiotic: true,
            manufacturingDate: "03/05/2024",
            expiryDate: "03/05/2026",
            image: null,
        },
        {
            medicineName: "Ibuprofen",
            batchNumber: "IBU202404",
            quantity: 180,
            costPrice: 1.2,
            sellingPrice: 2.5,
            category: "Tablet",
            antibiotic: false,
            manufacturingDate: "04/01/2024",
            expiryDate: "04/01/2026",
            image: null,
        },
        {
            medicineName: "Azithromycin",
            batchNumber: "AZI202405",
            quantity: 90,
            costPrice: 4.0,
            sellingPrice: 8.0,
            category: "Tablet",
            antibiotic: true,
            manufacturingDate: "05/10/2024",
            expiryDate: "05/10/2026",
            image: null,
        },
        {
            medicineName: "Metronidazole",
            batchNumber: "MET202406",
            quantity: 120,
            costPrice: 2.0,
            sellingPrice: 4.0,
            category: "Tablet",
            antibiotic: true,
            manufacturingDate: "06/15/2024",
            expiryDate: "06/15/2026",
            image: null,
        },
        {
            medicineName: "Cetirizine",
            batchNumber: "CET202407",
            quantity: 250,
            costPrice: 0.8,
            sellingPrice: 1.5,
            category: "Tablet",
            antibiotic: false,
            manufacturingDate: "07/01/2024",
            expiryDate: "07/01/2026",
            image: null,
        },
        {
            medicineName: "Erythromycin",
            batchNumber: "ERY202408",
            quantity: 130,
            costPrice: 3.5,
            sellingPrice: 7.0,
            category: "Tablet",
            antibiotic: true,
            manufacturingDate: "08/05/2024",
            expiryDate: "08/05/2026",
            image: null,
        },
        {
            medicineName: "Loratadine",
            batchNumber: "LOR202409",
            quantity: 175,
            costPrice: 1.1,
            sellingPrice: 2.2,
            category: "Tablet",
            antibiotic: false,
            manufacturingDate: "09/10/2024",
            expiryDate: "09/10/2026",
            image: null,
        },
        {
            medicineName: "Doxycycline",
            batchNumber: "DOX202410",
            quantity: 95,
            costPrice: 2.8,
            sellingPrice: 5.6,
            category: "Capsule",
            antibiotic: true,
            manufacturingDate: "10/15/2024",
            expiryDate: "10/15/2026",
            image: null,
        },
        {
            medicineName: "Omeprazole",
            batchNumber: "OME202411",
            quantity: 160,
            costPrice: 1.9,
            sellingPrice: 3.8,
            category: "Capsule",
            antibiotic: false,
            manufacturingDate: "11/05/2024",
            expiryDate: "11/05/2026",
            image: null,
        },
        {
            medicineName: "Clarithromycin",
            batchNumber: "CLA202412",
            quantity: 110,
            costPrice: 4.2,
            sellingPrice: 8.4,
            category: "Tablet",
            antibiotic: true,
            manufacturingDate: "12/01/2024",
            expiryDate: "12/01/2026",
            image: null,
        },
        {
            medicineName: "Folic Acid",
            batchNumber: "FOL202413",
            quantity: 300,
            costPrice: 0.6,
            sellingPrice: 1.2,
            category: "Tablet",
            antibiotic: false,
            manufacturingDate: "01/01/2025",
            expiryDate: "01/01/2027",
            image: null,
        },
        {
            medicineName: "Penicillin V",
            batchNumber: "PEN202414",
            quantity: 140,
            costPrice: 2.7,
            sellingPrice: 5.4,
            category: "Tablet",
            antibiotic: true,
            manufacturingDate: "02/20/2025",
            expiryDate: "02/20/2027",
            image: null,
        },
        {
            medicineName: "Vitamin C",
            batchNumber: "VIT202415",
            quantity: 220,
            costPrice: 0.9,
            sellingPrice: 1.8,
            category: "Tablet",
            antibiotic: false,
            manufacturingDate: "03/15/2025",
            expiryDate: "03/15/2027",
            image: null,
        },
    ];

    const showModal = ref(false);
</script>

<template>
    <div class="h-screen relative flex flex-col flex-1 overflow-hidden">
        <div
            class="hidden w-full md:absolute top-0 z-40 bg-gray-900 md:top-0 md:block p-3"
        >
            <h1
                class="text-gray-300 text-center text-lg font-styleScript md:text-2xl"
            >
                Orders Hub
            </h1>
        </div>
        <div class="overflow-auto overscroll-contain w-full">
            <div class="mx-auto container p-3">
                <div
                    class="max-h-[80vh] overflow-x-auto overscroll-contain mt-2 md:mt-14 mx-auto"
                >
                    <table class="text-sm text-left text-gray-400 w-full">
                        <thead
                            class="text-xs uppercase bg-gray-700 text-gray-400"
                        >
                            <tr>
                                <th class="px-6 py-4 whitespace-nowrap">
                                    Medicine Name
                                </th>
                                <th class="px-6 py-4 whitespace-nowrap">
                                    Batch Number
                                </th>
                                <th class="px-6 py-4 whitespace-nowrap">
                                    Quantity
                                </th>
                                <th class="px-6 py-4 whitespace-nowrap">
                                    Cost Price
                                </th>
                                <th class="px-6 py-4 whitespace-nowrap">
                                    Selling Price
                                </th>
                                <th class="px-6 py-4 whitespace-nowrap">
                                    Category
                                </th>
                                <th class="px-6 py-4 whitespace-nowrap">
                                    Antibiotic
                                </th>
                                <th class="px-6 py-4 whitespace-nowrap">
                                    Manufacturing Date
                                </th>
                                <th class="p-2 whitespace-nowrap">
                                    Expiry Date
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="medication in medicines"
                                :key="medication.id"
                                class="border-b bg-gray-800 border-gray-700 hover:bg-gray-600"
                            >
                                <td
                                    class="px-6 py-4 font-medium text-white whitespace-nowrap"
                                >
                                    {{ medication.medicineName }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    {{ medication.batchNumber }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    {{ medication.quantity }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    GH₵{{ medication.costPrice }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    GH₵{{ medication.sellingPrice }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    {{ medication.category }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    {{ medication.antibiotic ? "Yes" : "No" }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    {{ medication.manufacturingDate }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    {{ medication.expiryDate }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>
