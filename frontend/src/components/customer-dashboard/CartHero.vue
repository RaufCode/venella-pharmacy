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

    const cart = ref(!false);
</script>

<template>
    <div class="h-screen relative flex flex-col flex-1 overflow-hidden">
        <div
            class="hidden md:block w-full md:absolute top-0 z-50 p-3 bg-gray-900"
        >
            <h1
                class="text-gray-300 font-styleScript text-center text-lg md:text-2xl"
            >
                Welcome, Jane Doe
            </h1>
        </div>

        <div class="mx-auto container m-4 md:mt-[75px]">
            <!-- Empty Cart -->
            <div v-if="cart === false" class="text-center text-gray-500 mt-20">
                <i
                    class="pi pi-cart-plus text-5xl animate-pulse text-gray-400 mb-4"
                ></i>
                <p class="text-lg font-medium text-gray-700">
                    Your cart is currently empty!
                </p>
                <p class="text-sm text-gray-500">
                    Browse our medications and add what you need to start your
                    order.
                </p>
            </div>
            <!--Loaded Cart-->
            <div v-else class="p-3">
                <div
                    class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3"
                >
                    <div class="p-3 bg-white rounded-lg text-justify">
                        <div class="grid grid-cols-2 gap-3 mb-1">
                            <img
                                src="https://i.pravatar.cc/100?img=3"
                                alt=""
                                class="rounded-lg object-cover"
                            />
                            <div class="flex items-center justify-center">
                                <p
                                    class="font-semibold text-xl text-center text-green-600 overflow-hidden text-ellipsis whitespace-nowrap"
                                >
                                    ₵ 160
                                </p>
                            </div>
                        </div>
                        <div>
                            <h1
                                class="font-semibold text-gray-600 overflow-hidden text-ellipsis whitespace-nowrap"
                            >
                                Paracetamol okaydhjgfdshgfds
                            </h1>
                            <p
                                class="text-sm text-gray-500 overflow-hidden text-ellipsis mb-1"
                            >
                                Effective pain relief for fever and headaches...
                            </p>
                        </div>
                        <div class="flex items-center justify-between gap-4">
                            <div
                                class="flex items-center w-max border rounded-lg"
                            >
                                <button class="px-3 py-1 text-gray-600">
                                    −
                                </button>
                                <span class="px-4">1</span>
                                <button class="px-3 py-1 text-gray-600">
                                    +
                                </button>
                            </div>
                            <button class="text-red-500 hover:text-red-700">
                                <i class="pi pi-times-circle text-xl"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <!--checkout-->
                <div
                    class="p-4 bg-white rounded-xl shadow-md space-y-4 w-full max-w-sm mx-auto mt-4"
                >
                    <h2 class="font-bold text-gray-800">CART SUMMARY</h2>
                    <div class="flex items-center justify-between">
                        <span class="text-gray-600 text-base font-medium"
                            >Subtotal</span
                        >
                        <span class="font-semibold text-orange-600"
                            >GH₵ 6,372.00</span
                        >
                    </div>
                    <p class="text-sm text-gray-500">
                        Delivery fees not included
                    </p>
                    <div
                        class="bg-green-50 border border-green-200 text-oran-700 px-3 py-2 rounded-md text-sm"
                    >
                        <strong class="block font-medium">Free delivery</strong>
                        Free delivery on Express items
                    </div>
                    <button
                        class="w-full bg-orange-600 text-white py-3 font-semibold text-base hover:bg-orange-500 transition"
                    >
                        Checkout (GH₵ 6,372.00)
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
