<script setup>
    import { ref, computed } from "vue";
    import Btn from "@/components/ui/Btn.vue";
    import router from "@/router";
    const details = () => {
        router.push("/details");
    };
    const items = ref([
        {
            name: "Paracetamol",
            description: "Pain & fever relief",
            price: 160,
            quantity: 1,
        },
        {
            name: "Ibuprofen",
            description: "Anti-inflammatory",
            price: 200,
            quantity: 12,
        },
        {
            name: "Ciprofloxacin",
            description: "Antibiotic",
            price: 250,
            quantity: 5,
        },
        {
            name: "Azithromycin",
            description: "Antibiotic",
            price: 400,
            quantity: 3,
        },
    ]);

    const total = computed(() =>
        items.value.reduce((acc, item) => acc + item.price * item.quantity, 0)
    );

    const delivery = 15;

    const form = ref({
        name: "",
        phone: "",
        address: "",
    });

    const placeOrder = () => {
        alert(
            `Order placed successfully!\n\nName: ${form.value.name}\nPhone: ${
                form.value.phone
            }\nAddress: ${form.value.address}\nTotal: ₵${
                total.value + delivery
            }`
        );
        console.log("Order details:", form.value, items.value);
    };

    const goBack = () => {
        // If history length > 1, go back, else redirect to home
        if (window.history.length > 1) {
            router.back();
        } else {
            router.push("/"); // fallback route, adjust if needed
        }
    };
</script>

<template>
    <div class="h-screen w-full">
        <div
            class="min-h-screen md:flex items-center justify-center bg-gray-100 p-4 mb-0"
        >
            <div
                class="max-w-3xl w-full bg-gray-100 rounded-xl shadow-md overflow-hidden mx-auto"
            >
                <div class="p-2 md:p-6">
                    <!-- Go Back Button -->
                    <button
                        type="button"
                        @click="goBack"
                        aria-label="Go back"
                        class="flex items-center text-gray-600 hover:text-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-600 transition mb-4"
                    >
                        <i class="pi pi-arrow-left mr-2"></i> Go Back
                    </button>

                    <div class="grid md:grid-cols-2 gap-6">
                        <!-- Summary -->
                        <div class="p-4 md:p-6 bg-green-50 rounded-md">
                            <h2
                                class="text-xl font-semibold text-green-600 mb-2"
                            >
                                Order Summary
                            </h2>
                            <ul
                                class="space-y-4 max-h-60 overflow-y-auto overscroll-contain"
                            >
                                <li
                                    v-for="item in items"
                                    :key="item.name"
                                    class="flex justify-between items-start gap-3"
                                >
                                    <div>
                                        <h3
                                            class="font-medium text-gray-700 whitespace-nowrap text-ellipsis"
                                        >
                                            {{ item.name }}
                                        </h3>
                                        <p
                                            class="text-sm text-gray-500 whitespace-nowrap text-ellipsis"
                                        >
                                            {{ item.description }}
                                        </p>
                                    </div>
                                    <p class="text-green-600 font-semibold">
                                        ₵ {{ item.price }} x {{ item.quantity }}
                                    </p>
                                </li>
                            </ul>
                            <div class="border-t mt-4 pt-4">
                                <div
                                    class="flex justify-between gap-3 text-gray-600 font-medium"
                                >
                                    <span>Subtotal</span>
                                    <span>₵ {{ total }}</span>
                                </div>
                                <div
                                    class="flex justify-between gap-3 text-gray-600 font-medium"
                                >
                                    <span>Delivery</span>
                                    <span>₵ {{ delivery }}</span>
                                </div>
                                <div
                                    class="flex justify-between text-lg font-bold text-gray-600 mt-2"
                                >
                                    <span>Total</span>
                                    <span>₵ {{ total + delivery }}</span>
                                </div>
                            </div>
                        </div>

                        <!-- Delivery Details -->
                        <div class="p-4 bg-white rounded">
                            <h2
                                class="text-xl font-semibold text-orange-600 mb-4"
                            >
                                Delivery Information
                            </h2>
                            <form
                                @submit.prevent="placeOrder"
                                class="space-y-4"
                            >
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
                                        >Full Name</label
                                    >
                                    <input
                                        type="text"
                                        v-model="form.name"
                                        required
                                        class="mt-1 w-full border border-gray-400 rounded px-3 py-2 outline-none focus:border-orange-700"
                                    />
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
                                        >Phone Number</label
                                    >
                                    <input
                                        type="tel"
                                        v-model="form.phone"
                                        required
                                        class="mt-1 w-full border border-gray-400 rounded px-3 py-2 outline-none focus:border-orange-700"
                                    />
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
                                        >Delivery Address</label
                                    >
                                    <textarea
                                        v-model="form.address"
                                        required
                                        rows="3"
                                        class="mt-1 w-full border border-gray-400 rounded px-3 py-2 outline-none focus:border-orange-700 resize-none"
                                    ></textarea>
                                </div>
                                <Btn btnName="Confirm Order" @click="details" />
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
