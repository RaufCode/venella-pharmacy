<script setup>
    import { ref, computed, onMounted } from "vue";
    import { useMedStore } from "@/stores/medStore";

    const medStore = useMedStore();

    onMounted(() => {
        medStore.fetchProducts();
        medStore.fetchCategories();
    });

    function closeAddModal() {
        medStore.showModal = false;
        medStore.resetForm();
    }

    // Pagination logic
    const currentPage = ref(1);
    const productsPerPage = 6;

    const paginatedProducts = computed(() => {
        const start = (currentPage.value - 1) * productsPerPage;
        const end = start + productsPerPage;
        return medStore.products.slice(start, end);
    });

    const totalPages = computed(() => {
        return Math.ceil(medStore.products.length / productsPerPage);
    });

    const goToPage = (page) => {
        if (page >= 1 && page <= totalPages.value) {
            currentPage.value = page;
        }
    };

    const nextPage = () => goToPage(currentPage.value + 1);
    const prevPage = () => goToPage(currentPage.value - 1);
</script>

<template>
    <div class="h-screen w-full flex flex-col">
        <!-- Top Bar -->
        <div class="hidden md:block p-4 shadow font-semibold">
            <h1 class="text-3xl font-medium text-gray-600 font-styleScript">
                Medications Hub
            </h1>
        </div>

        <!-- Main Content -->
        <div class="p-4 overflow-y-auto flex-grow">
            <div
                class="p-0 lg:p-4 lg:shadow lg:bg-gray-50 lg:rounded-lg lg:h-full overflow-y-auto"
            >
                <!-- Medication Table -->
                <div class="overflow-x-auto rounded-lg border bg-white">
                    <table
                        v-if="medStore.hasProducts"
                        class="min-w-full divide-y divide-gray-200"
                    >
                        <thead class="bg-gray-200 text-gray-600 text-sm">
                            <tr>
                                <th class="px-6 py-3 text-left">Name</th>
                                <th class="px-6 py-3 text-left">Price(₵)</th>
                                <th class="px-6 py-3 text-left">Stock</th>
                                <th class="px-6 py-3 text-left">Category</th>
                            </tr>
                        </thead>
                        <tbody
                            class="divide-y divide-gray-100 text-sm font-medium"
                        >
                            <tr
                                v-for="product in paginatedProducts"
                                :key="product.id"
                                class="hover:bg-gray-100 transition"
                            >
                                <td class="px-6 py-3 text-gray-700 truncate">
                                    {{ product.name }}
                                </td>
                                <td class="px-6 py-3 text-red-600">
                                    {{ product.price }}
                                </td>
                                <td class="px-6 py-3 text-blue-600">
                                    {{ product.stock }}
                                </td>
                                <td class="px-6 py-3 text-gray-600">
                                    {{ product.category.name }}
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <div v-else class="text-center p-10 text-gray-500">
                        <i class="pi pi-box text-4xl mb-2"></i>
                        <p>No medications found.</p>
                    </div>
                </div>

                <!-- Pagination -->
                <div
                    v-if="totalPages > 1"
                    class="flex justify-center items-center gap-4 my-4"
                >
                    <button
                        @click="prevPage"
                        :disabled="currentPage === 1"
                        class="px-4 py-2 text-sm border rounded disabled:opacity-50 bg-white"
                    >
                        <i class="pi pi-angle-double-left"></i>
                    </button>

                    <span class="text-sm font-medium">
                        {{ currentPage }} of {{ totalPages }}
                    </span>

                    <button
                        @click="nextPage"
                        :disabled="currentPage === totalPages"
                        class="px-4 py-2 text-sm border rounded disabled:opacity-50 bg-white"
                    >
                        <i class="pi pi-angle-double-right"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
