<script setup>
    import { ref, computed } from "vue";
    import router from "@/router";

    // Sample cart data
    const cartItems = ref([
        {
            id: 1,
            name: "Paracetamol",
            price: 16,
            quantity: 2,
            image: "https://source.unsplash.com/100x100/?medicine",
        },
        {
            id: 2,
            name: "Ibuprofen",
            price: 10,
            quantity: 1,
            image: "https://cdn.pixabay.com/photo/2016/11/29/09/08/medicine-1869590_1280.jpg",
        },
        {
            id: 3,
            name: "Amoxicillin",
            price: 22,
            quantity: 1,
            image: "https://source.unsplash.com/100x100/?pharmacy",
        },
    ]);

    const goBack = () => {
        router.back();
    };

    const redirectToCheckout = () => {
        router.push("/checkout");
    };

    const increase = (item) => {
        item.quantity++;
    };

    const decrease = (item) => {
        if (item.quantity > 1) item.quantity--;
    };

    const removeItem = (id) => {
        cartItems.value = cartItems.value.filter((item) => item.id !== id);
    };

    const subtotal = computed(() =>
        cartItems.value.reduce(
            (sum, item) => sum + item.price * item.quantity,
            0
        )
    );
</script>

<template>
    <div class="min-h-screen flex flex-col bg-gray-50">
        <!-- Header -->
        <header
            class="bg-gray-900 text-white p-4 flex items-center gap-4 sticky top-0 z-50"
        >
            <button @click="goBack" class="hover:text-orange-400 transition">
                <i class="pi pi-arrow-left text-lg"></i>
            </button>
            <h1 class="text-base md:text-xl font-semibold">Your Cart</h1>
        </header>

        <!-- Main Content -->
        <main
            class="flex flex-col lg:flex-row gap-4 p-4 md:p-6 flex-grow container mx-auto"
        >
            <!-- Cart Items -->
            <section class="flex-1 space-y-3 md:space-y-4">
                <div
                    v-for="item in cartItems"
                    :key="item.id"
                    class="bg-white rounded-lg shadow-md p-3 md:p-4 flex items-center gap-3 md:gap-4"
                >
                    <img
                        :src="cartItems.image"
                        alt=""
                        class="w-14 h-14 md:w-20 md:h-20 object-cover rounded-md"
                    />

                    <div class="flex-1">
                        <h2
                            class="font-medium text-gray-800 text-sm md:text-base"
                        >
                            {{ item.name }}
                        </h2>
                        <p class="text-xs md:text-base text-gray-500">
                            ₵ {{ item.price.toFixed(2) }}
                        </p>

                        <div class="mt-2 flex items-center gap-2 md:gap-3">
                            <button
                                @click="decrease(item)"
                                class="bg-gray-200 px-2 py-1 rounded hover:bg-gray-300 text-xs md:text-base"
                            >
                                −
                            </button>
                            <span class="font-semibold text-sm md:text-base">{{
                                item.quantity
                            }}</span>
                            <button
                                @click="increase(item)"
                                class="bg-gray-200 px-2 py-1 rounded hover:bg-gray-300 text-xs md:text-base"
                            >
                                +
                            </button>
                        </div>
                    </div>

                    <div
                        class="flex flex-col items-center gap-5 text-xs md:text-base"
                    >
                        <p class="text-orange-600 font-bold">
                            ₵{{ (item.price * item.quantity).toFixed(2) }}
                        </p>
                        <button
                            @click="removeItem(item.id)"
                            class="text-red-500 hover:text-red-700 mt-2 text-xs"
                        >
                            <i class="pi pi-trash"></i>
                        </button>
                    </div>
                </div>

                <div
                    v-if="cartItems.length === 0"
                    class="text-center text-gray-500 mt-10 text-sm md:text-base"
                >
                    <p>
                        <i
                            class="pi pi-cart-plus text-3xl md:text-5xl animate-pulse"
                        ></i>
                    </p>
                    <h1 class="font-medium text-gray-600 text-base md:text-lg">
                        Your cart is empty
                    </h1>
                    <p>Items added to the cart will appear here</p>
                </div>
            </section>

            <!-- Cart Summary -->
            <aside
                v-if="cartItems.length > 0"
                class="w-full lg:w-[300px] bg-white p-4 md:p-6 rounded-lg shadow-md space-y-3 md:space-y-4 h-max text-sm md:text-base lg:text-lg"
            >
                <h2 class="text-base md:text-xl font-semibold text-gray-800">
                    Cart Summary
                </h2>

                <div class="flex justify-between">
                    <span class="text-gray-600">Subtotal</span>
                    <span class="font-semibold text-orange-600"
                        >GH₵ {{ subtotal.toFixed(2) }}</span
                    >
                </div>

                <p class="text-xs md:text-sm text-gray-500">
                    Delivery fees not included
                </p>

                <div
                    class="bg-green-50 border border-green-200 p-3 rounded-md text-xs md:text-sm lg:text-base text-green-700"
                >
                    <strong>Free delivery</strong> on Express items
                </div>

                <button
                    @click="redirectToCheckout"
                    :disabled="cartItems.length === 0"
                    class="w-full bg-orange-600 text-white py-2 md:py-3 rounded-md font-medium hover:bg-orange-500 transition disabled:opacity-50 disabled:cursor-not-allowed text-sm md:text-base"
                >
                    Checkout (GH₵ {{ subtotal.toFixed(2) }})
                </button>
            </aside>
        </main>
    </div>
</template>
