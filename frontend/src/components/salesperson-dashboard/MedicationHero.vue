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
    const productsPerPage = 3;

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
    <div class="h-screen w-full relative flex flex-col">
        <!-- Top Bar -->
        <div
            class="hidden md:flex justify-between items-center bg-gray-900 p-4 shadow-md"
        >
            <h1 class="text-white text-xl">Medication Management</h1>
        </div>

        <!-- Main Content -->
        <div class="p-4 overflow-y-auto flex-grow">
            <!-- Medication Table -->
            <div class="overflow-x-auto rounded-lg shadow border bg-white">
                <table
                    v-if="medStore.hasProducts"
                    class="min-w-full divide-y divide-gray-200"
                >
                    <thead class="bg-gray-800 text-white text-sm">
                        <tr>
                            <th class="px-6 py-3 text-left">Name</th>
                            <th class="px-6 py-3 text-left">Price</th>
                            <th class="px-6 py-3 text-left">Stock</th>
                            <th class="px-6 py-3 text-left">Category</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200 text-sm">
                        <tr
                            v-for="product in paginatedProducts"
                            :key="product.id"
                            class="hover:bg-gray-100 transition"
                        >
                            <td class="px-6 py-3">{{ product.name }}</td>
                            <td class="px-6 py-3 text-green-600 font-bold">
                                ₵{{ product.price }}
                            </td>
                            <td class="px-6 py-3">{{ product.stock }}</td>
                            <td class="px-6 py-3">
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
                class="flex justify-center items-center gap-4 mt-6"
            >
                <button
                    @click="prevPage"
                    :disabled="currentPage === 1"
                    class="px-4 py-2 text-sm border rounded disabled:opacity-50"
                >
                    Previous
                </button>

                <span class="text-sm font-medium">
                    {{ currentPage }} of {{ totalPages }}
                </span>

                <button
                    @click="nextPage"
                    :disabled="currentPage === totalPages"
                    class="px-4 py-2 text-sm border rounded disabled:opacity-50"
                >
                    Next
                </button>
            </div>
        </div>
    </div>
</template>
