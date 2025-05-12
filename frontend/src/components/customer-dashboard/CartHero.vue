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
        router.push("/checkout");
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
                Cart Summary
            </h1>
        </div>

        <div class="overflow-y-auto overscroll-contain w-full">
            <div class="mx-auto container md:pt-14 py-3 pb-14 md:pb-0">
                <!-- Empty Cart -->
                <div
                    v-if="cart === !false"
                    class="text-center text-gray-500 mt-20"
                >
                    <i
                        class="pi pi-cart-plus text-5xl animate-pulse text-gray-400 mb-4"
                    ></i>
                    <p class="text-lg font-medium text-gray-700">
                        Your cart is currently empty!
                    </p>
                    <p class="text-sm text-gray-500">
                        Browse our medications and add what you need to start
                        your order
                    </p>
                </div>
                <!--Loaded Cart-->
                <div v-else class="p-3">
                    <div
                        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3"
                    >
                        <div
                            v-for="cart in carts"
                            :key="cart.id"
                            class="bg-white p-4 shadow hover:shadow-md rounded-lg text-justify"
                        >
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
                                        {{ cart.price }}
                                    </p>
                                </div>
                            </div>
                            <div>
                                <h1
                                    class="font-semibold text-gray-600 overflow-hidden text-ellipsis whitespace-nowrap"
                                >
                                    {{ cart.name }}
                                </h1>
                                <p
                                    class="text-sm text-gray-500 overflow-hidden text-ellipsis whitespace-nowrap mb-1"
                                >
                                    {{ cart.description }}
                                </p>
                            </div>
                            <div
                                class="flex items-center justify-between gap-4"
                            >
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
                        class="p-4 bg-white rounded-xl shadow-md space-y-4 w-full max-w-sm mx-auto mt-3"
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
                            <strong class="block font-medium"
                                >Free delivery</strong
                            >
                            Free delivery on Express items
                        </div>
                        <button
                            @click="redirect"
                            class="w-full bg-orange-600 text-white py-3 font-semibold text-base hover:bg-orange-500 transition"
                        >
                            Checkout (GH₵ 6,372.00)
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
