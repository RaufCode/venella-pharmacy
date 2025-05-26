<script setup>
    import { ref } from "vue";

    const product = ref({
        name: "AILYONS TYB-201-A-S",
        description:
            "AILYONS TYB-201-A-S is a high-quality product designed for everyday use. It features a sleek design and durable materials, making it perfect for both home and professional settings.",
        brand: "AILYONS",
        price: 199,
        oldPrice: 378,
        discount: 47,
        ratings: 721,
        image: "/drug2.jpg", // Replace with actual path
        variations: ["TYB-201-A White", "TYB-202-B Black"],
    });

    const selectedVariation = ref(product.value.variations[0]);
</script>
<template>
    <div
        class="min-h-screen bg-gray-50 p-4 sm:p-6 lg:p-12 flex items-center justify-center"
    >
        <!-- Wrapper -->
        <div class="max-w-6xl w-full">
            <!-- Go Back Button -->
            <button
                @click="$router.back()"
                class="text-orange-600 text-sm font-medium flex items-center gap-1"
            >
                <i class="pi pi-arrow-left mr-2"></i>
                Go Back
            </button>
            <!-- Centered container -->
            <div class="flex flex-col lg:flex-row gap-8 p-5">
                <!-- Left: Product Image -->
                <div class="flex-1">
                    <img
                        :src="product.image"
                        :alt="product.name"
                        class="w-full max-h-[400px] object-contain rounded-xl"
                    />
                </div>

                <!-- Right: Info & Actions -->
                <div class="w-full lg:w-[450px] space-y-4 text-sm sm:text-base">
                    <!-- Store Tags -->
                    <div class="flex items-center gap-2">
                        <span
                            class="bg-orange-100 text-orange-600 px-3 py-1 rounded-full text-xs font-medium"
                        >
                            Official Store
                        </span>
                        <span
                            class="bg-pink-100 text-pink-600 px-3 py-1 rounded-full text-xs font-medium"
                        >
                            Anniversary Deal
                        </span>
                    </div>

                    <!-- Product Name -->
                    <h1 class="font-semibold text-gray-800 leading-snug">
                        {{ product.name }}
                    </h1>
                    <h1 class="text-gray-800 leading-snug text-justify">
                        {{ product.description }}
                    </h1>

                    <!-- Add to Cart -->
                    <button
                        class="bg-orange-600 hover:bg-orange-700 text-white py-2 px-4 sm:py-3 sm:px-6 rounded w-full text-sm sm:text-base font-medium"
                    >
                        <i class="pi pi-cart-plus mr-2"></i> Add to Cart
                    </button>

                    <!-- Price -->
                    <div>
                        <p class="text-orange-600 font-bold">
                            GH₵ {{ product.price }}
                        </p>
                        <p class="text-green-600 text-sm font-medium">
                            {{ product.discount }}% OFF
                        </p>
                        <p class="text-red-600 text-sm">Few units left</p>
                    </div>

                    <!-- Delivery Info -->
                    <div class="bg-gray-100 p-3 rounded-md text-sm">
                        <p class="text-green-700 font-semibold">
                            Delivery is not free
                        </p>
                    </div>

                    <!-- Ratings -->
                    <div
                        class="flex items-center text-yellow-500 gap-1 text-sm"
                    >
                        <i class="pi pi-star-fill" v-for="n in 4" :key="n"></i>
                        <i class="pi pi-star"></i>
                        <span class="text-gray-600 ml-2">
                            ({{ product.ratings }} verified ratings)
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
