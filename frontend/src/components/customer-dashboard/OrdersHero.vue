<script setup>
    import { ref } from "vue";
    import router from "@/router";

    const carts = [
        {
            price: "₵ 160",
            name: "Paracetamol",
            description: "Effective pain relief for fever and headaches...",
        },
        {
            price: "₵ 85",
            name: "Ibuprofen",
            description: "Relieves inflammation, pain, and reduces fever.",
        },
        {
            price: "₵ 210",
            name: "Ciprofloxacin",
            description: "Used to treat bacterial infections effectively.",
        },
        {
            price: "₵ 75",
            name: "Cetirizine",
            description: "Provides relief from allergies and hay fever.",
        },
        {
            price: "₵ 320",
            name: "Azithromycin",
            description: "Broad-spectrum antibiotic for serious infections.",
        },
        {
            price: "₵ 60",
            name: "Vitamin C",
            description: "Boosts immune system and prevents deficiency.",
        },
        {
            price: "₵ 110",
            name: "Metronidazole",
            description: "Treats bacterial and parasitic infections.",
        },
        {
            price: "₵ 185",
            name: "Amoxicillin",
            description: "A widely used antibiotic for various infections.",
        },
        {
            price: "₵ 140",
            name: "Loratadine",
            description: "Non-drowsy antihistamine for allergies.",
        },
        {
            price: "₵ 90",
            name: "Omeprazole",
            description: "Reduces stomach acid to treat ulcers and GERD.",
        },
    ];

    const cart = ref(false);
    const redirect = () => {
        router.push("/login");
    };
</script>

<template>
    <div class="h-screen w-full relative flex flex-col flex-1 overflow-hidden">
        <div
            class="hidden md:block w-full md:absolute top-0 z-50 p-3 bg-gray-900"
        >
            <h1
                class="text-gray-300 font-styleScript text-center text-lg md:text-2xl"
            >
                Order History
            </h1>
        </div>

        <div class="overflow-auto overscroll-contain w-full mb-14 md:mb-0">
            <div class="mx-auto container md:pt-14 p-3">
                <!-- Empty Cart -->
                <div
                    v-if="cart === !false"
                    class="text-center text-gray-500 mt-20"
                >
                    <i
                        class="pi pi-shopping-cart text-5xl animate-pulse text-gray-400 mb-4"
                    ></i>
                    <p class="text-lg font-medium text-gray-700">
                        You haven't placed an order yet!
                    </p>
                    <p class="text-sm text-gray-500">
                        Once you start shopping, your order history will appear
                        here for easy tracking and reference.
                    </p>
                </div>
                <!--Loaded Cart-->
                <div v-else class="p-0 md:py-3">
                    <div class="">
                        <table class="min-w-full border bg-white text-center">
                            <thead>
                                <tr
                                    class="bg-gray-300 text-gray-600 font-semibold text-sm uppercase tracking-wider"
                                >
                                    <th class="px-6 py-2">Product</th>
                                    <th class="px-6 py-2">Price</th>
                                    <th class="px-6 py-2">Quantity</th>
                                    <th class="px-6 py-2">Delete</th>
                                </tr>
                            </thead>
                            <tbody class="text-black text-sm font-light">
                                <tr class="hover:bg-gray-50">
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        prduct name
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        ₵ 160
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        2
                                    </td>
                                    <td>
                                        <button class="block mx-auto">
                                            <i
                                                class="pi pi-trash text-red-600 text-2xl"
                                            ></i>
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
