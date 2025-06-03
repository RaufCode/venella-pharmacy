<script setup>
    import { onMounted, ref } from "vue";
    import { useMedStore } from "@/stores/medStore";
    import InputField from "@/components/InputField.vue";
    import Btn from "@/components/Btn.vue";

    const medStore = useMedStore();
    const {
        products,
        categories,
        showModal,
        isSubmitting,
        editingProductId,
        form,
        hasProducts,
        isEditing,
        fetchProducts,
        fetchCategories,
        submitForm,
        editProduct,
        deleteProduct,
        resetForm,
        handleImageUpload,
    } = medStore;

    // Modal state
    function openModal() {
        showModal.value = true;
    }
    function closeModal() {
        resetForm();
        showModal.value = false;
    }

    onMounted(async () => {
        await fetchCategories();
        await fetchProducts();
    });
</script>

<template>
    <div class="h-screen w-full relative flex flex-col flex-1 overflow-hidden">
        <!-- Top Bar -->
        <div
            class="hidden w-full md:absolute top-0 z-40 bg-gray-900 shadow-md md:flex justify-between items-center p-3"
        >
            <h1 class="text-gray-300 font-styleScript text-lg md:text-2xl">
                Medication Manager
            </h1>
            <button
                @click="openModal"
                class="py-2 px-4 bg-orange-600 text-sm text-white font-medium hover:bg-orange-500"
            >
                Add Medication
            </button>
        </div>

        <!-- Main Content -->
        <div class="overflow-y-auto overscroll-contain w-full">
            <div class="mx-auto container p-3">
                <!-- Button (Mobile) -->
                <button
                    @click="openModal"
                    class="py-2 px-4 bg-orange-600 text-sm text-white font-medium hover:bg-orange-500 md:hidden"
                >
                    Add Medication
                </button>

                <!-- Medication Table -->
                <div
                    class="max-h-[80vh] overflow-x-auto overscroll-contain mt-2 md:mt-14 mx-auto rounded-lg shadow-lg border border-gray-200 bg-white"
                >
                    <table
                        v-if="products.length > 0"
                        class="min-w-full divide-y divide-gray-200 table-auto"
                    >
                        <thead class="bg-gray-800 sticky top-0 z-10">
                            <tr>
                                <th
                                    class="px-6 py-3 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider truncate"
                                >
                                    Name
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-semibold text-orange-400 uppercase tracking-wider truncate"
                                >
                                    Category
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-semibold text-indigo-400 uppercase tracking-wider truncate"
                                >
                                    Stock
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-semibold text-green-400 uppercase tracking-wider truncate"
                                >
                                    Price
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider truncate"
                                >
                                    Description
                                </th>
                                <th
                                    class="px-6 py-3 text-center text-xs font-semibold text-gray-300 uppercase tracking-wider"
                                >
                                    Update
                                </th>
                                <th
                                    class="px-6 py-3 text-center text-xs font-semibold text-gray-300 uppercase tracking-wider"
                                >
                                    Delete
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr
                                v-for="med in products"
                                :key="med.id"
                                class="hover:bg-gray-50 transition-colors duration-150 cursor-pointer"
                                :title="med.name"
                            >
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900 truncate max-w-xs"
                                >
                                    <div class="flex items-center gap-2">
                                        <img
                                            v-if="
                                                med.images && med.images.length
                                            "
                                            :src="med.images[0].image"
                                            alt="product"
                                            class="w-8 h-8 object-cover rounded"
                                        />
                                        <span>{{ med.name }}</span>
                                    </div>
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-orange-600 truncate max-w-md"
                                >
                                    {{ med.category?.name || "-" }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-indigo-600 font-bold truncate max-w-xs"
                                >
                                    {{ med.stock }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-green-700 font-semibold truncate max-w-xs"
                                >
                                    ₵{{ med.price }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 truncate max-w-sm"
                                >
                                    {{ med.description }}
                                </td>
                                <td class="px-6 py-4 text-center">
                                    <button
                                        @click="editProduct(med.id)"
                                        class="text-blue-600 hover:text-blue-800 text-xl transition"
                                        title="Edit medication"
                                        aria-label="Edit medication"
                                    >
                                        <i class="pi pi-file-edit"></i>
                                    </button>
                                </td>
                                <td class="px-6 py-4 text-center">
                                    <button
                                        @click="deleteProduct(med.id)"
                                        class="text-red-600 hover:text-red-800 text-xl transition"
                                        title="Delete medication"
                                        aria-label="Delete medication"
                                    >
                                        <i class="pi pi-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <div
                        v-if="products.length === 0"
                        class="text-center text-gray-500 mt-10 py-16"
                    >
                        <p>
                            <i
                                class="pi pi-box text-3xl md:text-5xl animate-pulse"
                            ></i>
                        </p>
                        <p>No medications found</p>
                    </div>
                </div>

                <!-- Modal -->
                <div
                    v-if="showModal"
                    class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50 p-4"
                >
                    <div
                        class="w-full max-w-xl max-h-[90vh] overflow-y-auto p-6 bg-white rounded-lg shadow-lg"
                    >
                        <form @submit.prevent="submitForm" class="space-y-6">
                            <div class="flex justify-between items-center">
                                <h2 class="text-xl font-bold text-gray-800">
                                    {{
                                        isEditing
                                            ? "Edit Medication"
                                            : "Add Medication"
                                    }}
                                </h2>
                                <button
                                    type="button"
                                    @click="closeModal"
                                    class="text-orange-600 text-2xl hover:text-orange-800 transition"
                                    aria-label="Close modal"
                                >
                                    <i class="pi pi-times"></i>
                                </button>
                            </div>
                            <!-- Name -->
                            <InputField
                                v-model="form.name"
                                labelname="Name"
                                class="w-full"
                                required
                            />
                            <!-- Category & Stock -->
                            <div class="md:flex gap-4">
                                <label
                                    class="flex-1 block mt-3 text-sm text-gray-900"
                                >
                                    Category
                                    <select
                                        v-model="form.category"
                                        class="mt-1 w-full border border-gray-400 rounded px-4 py-2 focus:outline-none focus:border-orange-700 bg-transparent"
                                        required
                                    >
                                        <option value="" disabled>
                                            Select category
                                        </option>
                                        <option
                                            v-for="cat in categories"
                                            :key="cat.id"
                                            :value="cat.id"
                                        >
                                            {{ cat.name }}
                                        </option>
                                    </select>
                                </label>
                                <InputField
                                    v-model="form.stock"
                                    labelname="Stock"
                                    type="number"
                                    class="flex-1"
                                    min="0"
                                    required
                                />
                            </div>
                            <!-- Price -->
                            <InputField
                                v-model="form.price"
                                labelname="Price"
                                type="number"
                                min="0"
                                class="w-full"
                                required
                            />
                            <!-- Description -->
                            <label class="block mt-3 text-sm text-gray-900">
                                Description
                                <textarea
                                    v-model="form.description"
                                    rows="2"
                                    class="mt-1 w-full border border-gray-400 rounded px-4 py-2 focus:outline-none focus:border-orange-700 bg-transparent resize-none"
                                    required
                                ></textarea>
                            </label>
                            <!-- Product Images -->
                            <label class="block mt-3 text-sm text-gray-900">
                                Product Images
                                <input
                                    type="file"
                                    multiple
                                    @change="handleImageUpload"
                                    class="mt-1 w-full border border-gray-400 rounded px-4 py-2 bg-white"
                                    accept="image/*"
                                />
                            </label>
                            <!-- Submit Button -->
                            <div>
                                <Btn
                                    :disabled="isSubmitting"
                                    :btnName="isEditing ? 'Update' : 'Save'"
                                />
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
