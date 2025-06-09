<script setup>
    import { onMounted } from "vue";
    import { useMedStore } from "@/stores/medStore";

    const medStore = useMedStore();

    onMounted(() => {
        medStore.fetchProducts();
        medStore.fetchCategories();
    });

    // Close modal handler
    function closeAddModal() {
        medStore.showModal = false;
        medStore.resetForm();
    }
</script>

<template>
    <div class="h-screen w-full flex flex-col">
        <!-- Top Bar -->
        <div
            class="hidden md:flex justify-between items-center bg-gray-50 w-full p-4 shadow static top-0 z-50"
        >
            <h1 class="text-gray-700 text-3xl font-styleScript">
                Medications Hub
            </h1>
            <button
                @click="medStore.showModal = true"
                class="bg-orange-600 hover:bg-orange-500 rounded-lg font-semibold text-white px-4 py-2"
            >
                Add Product
            </button>
        </div>

        <!-- Main Content -->
        <div class="p-4 overflow-y-auto flex-grow">
            <!-- Mobile Add Button -->
            <button
                @click="medStore.showModal = true"
                class="md:hidden mb-4 bg-orange-600 hover:bg-orange-500 text-white px-4 py-2 text-sm"
            >
                Add Product
            </button>

            <!-- Medication Table -->
            <div class="overflow-x-auto bg-white">
                <table
                    v-if="medStore.hasProducts"
                    class="min-w-full divide-y divide-gray-200"
                >
                    <thead class="bg-gray-200 text-gray-600 text-sm">
                        <tr>
                            <th class="px-6 py-3 text-left">Name</th>
                            <th class="px-6 py-3 text-left">Price(₵)</th>
                            <th class="px-6 py-3 text-left">Stock</th>
                            <th class="px-6 py-3 text-left">Brand</th>
                            <th class="px-6 py-3 text-center">Edit</th>
                            <th class="px-6 py-3 text-center">Delete</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100 text-sm font-medium">
                        <tr
                            v-for="product in medStore.products"
                            :key="product.id"
                            class="hover:bg-gray-50 transition hover:shadow-lg"
                        >
                            <td class="px-6 py-3 text-gray-700 truncate">
                                {{ product.name }}
                            </td>
                            <td class="px-6 py-3 text-green-600 font-bold">
                                {{ product.price }}
                            </td>
                            <td class="px-6 py-3">{{ product.stock }}</td>
                            <td class="px-6 py-3 text-gray-600 truncate">
                                {{ product.brand || "No Brand Name" }}
                            </td>
                            <td class="px-6 py-3 text-center">
                                <button
                                    @click="medStore.editProduct(product.id)"
                                    class="text-blue-600 hover:text-blue-800 text-lg"
                                    title="Edit"
                                    type="button"
                                >
                                    <i class="pi pi-pencil"></i>
                                </button>
                            </td>
                            <td class="px-6 py-3 text-center">
                                <button
                                    @click="medStore.deleteProduct(product.id)"
                                    class="text-red-600 hover:text-red-800 text-lg"
                                    title="Delete"
                                    type="button"
                                >
                                    <i class="pi pi-trash"></i>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <div v-else class="text-center p-10 text-gray-500">
                    <i class="pi pi-box text-4xl mb-2"></i>
                    <p>No medications found.</p>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div
            v-if="medStore.showModal"
            class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50 p-4"
        >
            <div
                class="w-full max-w-lg max-h-[90vh] overflow-y-auto bg-white p-6 rounded-lg shadow-lg"
            >
                <form @submit.prevent="medStore.submitForm" class="space-y-4">
                    <div class="flex justify-between items-center mb-3">
                        <h2 class="text-xl font-bold text-gray-800">
                            {{
                                medStore.isEditing
                                    ? "Edit Medication"
                                    : "Add Medication"
                            }}
                        </h2>
                        <button
                            type="button"
                            @click="closeAddModal"
                            class="text-orange-600 text-2xl hover:text-orange-800 transition"
                            aria-label="Close modal"
                        >
                            <i class="pi pi-times"></i>
                        </button>
                    </div>
                    <!-- Name & Stock -->
                    <div class="flex gap-3 flex-col sm:flex-row">
                        <label class="block flex-1 text-sm text-gray-700">
                            Name
                            <input
                                v-model="medStore.form.name"
                                type="text"
                                required
                                class="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-orange-600"
                            />
                        </label>
                        <label class="block flex-1 text-sm text-gray-700">
                            Brand
                            <input
                                v-model="medStore.form.brand"
                                required
                                class="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-orange-600"
                            />
                        </label>
                    </div>

                    <!-- Stock & Price -->
                    <div class="flex gap-3 flex-col sm:flex-row">
                        <label class="block flex-1 text-sm text-gray-700">
                            Stock
                            <input
                                v-model="medStore.form.stock"
                                type="number"
                                min="0"
                                required
                                class="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-orange-600"
                            />
                        </label>
                        <label class="block flex-1 text-sm text-gray-700">
                            Price
                            <input
                                v-model="medStore.form.price"
                                type="number"
                                min="0"
                                required
                                class="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-orange-600"
                            />
                        </label>
                    </div>
                    <!-- Category -->
                    <label class="block flex-1 text-sm text-gray-700">
                        Category
                        <select
                            v-model="medStore.form.category"
                            required
                            class="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-orange-600"
                        >
                            <option value="" disabled>Select category</option>
                            <option
                                v-for="cat in medStore.categories"
                                :key="cat.id"
                                :value="cat.id"
                            >
                                {{ cat.name }}
                            </option>
                        </select>
                    </label>
                    <!-- Description -->
                    <label class="block text-sm text-gray-700">
                        Description
                        <textarea
                            v-model="medStore.form.description"
                            rows="2"
                            required
                            class="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-orange-600 resize-none"
                        ></textarea>
                    </label>

                    <!-- Images (only show if NOT editing) -->
                    <div class="flex gap-3 flex-col sm:flex-row">
                        <label
                            v-if="!medStore.isEditing"
                            class="block text-sm text-gray-700"
                        >
                            Product Images
                            <input
                                type="file"
                                multiple
                                @change="medStore.handleImageUpload"
                                class="mt-1 w-full border border-gray-300 rounded px-3 py-2 bg-white"
                                accept="image/*"
                            />
                        </label>
                    </div>
                    <!-- Submit -->
                    <div>
                        <button
                            type="submit"
                            class="w-full bg-orange-600 text-white py-2 rounded font-semibold hover:bg-orange-700 transition"
                            :disabled="medStore.isSubmitting"
                        >
                            {{
                                medStore.isSubmitting
                                    ? "Saving..."
                                    : "Save Medication"
                            }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
