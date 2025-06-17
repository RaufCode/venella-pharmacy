<script setup>
    import { ref, computed, onMounted } from "vue";
    import {
        Search,
        Plus,
        Package,
        Pill,
        Edit,
        Trash2,
        ChevronLeft,
        ChevronRight,
    } from "lucide-vue-next";

    import BaseCard from "@/components/shared/BaseCard.vue";
    import BaseButton from "@/components/shared/BaseButton.vue";
    import BaseInput from "@/components/shared/BaseInput.vue";
    import MedicationModal from "@/components/modals/MedicationModal.vue";
    import Spinner from "@/components/ui/Spinner.vue";

    import { useMedStore } from "@/stores/medStore";

    const props = defineProps({
        userRole: {
            type: String,
            required: true,
        },
    });

    const medStore = useMedStore();

    const searchTerm = ref("");
    const currentPage = ref(1);
    const itemsPerPage = 10;
    const showAddModal = ref(false);
    const editingMedication = ref(null);

    const isLoading = computed(() => medStore.isLoading);
    const medications = computed(() => medStore.products || []);

    const filteredMedications = computed(() => {
        if (!searchTerm.value) return medications.value;

        return medications.value.filter(
            (medication) =>
                medication.name
                    .toLowerCase()
                    .includes(searchTerm.value.toLowerCase()) ||
                medication.category?.name
                    .toLowerCase()
                    .includes(searchTerm.value.toLowerCase())
        );
    });

    const totalPages = computed(() =>
        Math.ceil(filteredMedications.value.length / itemsPerPage)
    );

    const paginatedMedications = computed(() => {
        const start = (currentPage.value - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        return filteredMedications.value.slice(start, end);
    });

    const editMedication = (medication) => {
        editingMedication.value = medication;
    };

    const deleteMedication = async (id) => {
        if (confirm("Are you sure you want to delete this medication?")) {
            await medStore.deleteProduct(id);
        }
    };

    const closeModal = () => {
        showAddModal.value = false;
        editingMedication.value = null;
    };

    const handleMedicationSaved = () => {
        closeModal();
        medStore.fetchProducts();
    };

    onMounted(() => {
        medStore.fetchProducts();
        medStore.fetchCategories();
    });
</script>
<template>
    <div class="space-y-6">
        <Spinner v-if="medStore.isSubmitting || medStore.isLoading" />
        <!-- Header Actions -->
        <div
            class="flex flex-col sm:flex-row sm:items-center justify-between gap-4"
        >
            <div>
                <h2 class="text-xl text-gray-600">Inventory</h2>
            </div>

            <div class="flex items-center gap-3">
                <BaseInput
                    v-model="searchTerm"
                    placeholder="Search..."
                    size="sm"
                    class="w-64"
                >
                    <template #icon>
                        <Search class="w-4 h-4 text-gray-400" />
                    </template>
                </BaseInput>

                <BaseButton
                    v-if="userRole === 'admin'"
                    @click="showAddModal = true"
                    class="whitespace-nowrap"
                >
                    <template #icon>
                        <Plus class="w-4 h-4" />
                    </template>
                    Add
                </BaseButton>
            </div>
        </div>

        <!-- Medication Grid/Table -->
        <BaseCard>
            <div
                v-if="isLoading"
                class="flex items-center justify-center py-12"
            >
                <div
                    class="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"
                ></div>
            </div>

            <div
                v-else-if="filteredMedications.length === 0"
                class="text-center py-12"
            >
                <Package class="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <h3 class="text-lg font-medium text-gray-900">
                    No medications found
                </h3>
                <p class="text-gray-500">
                    Try adjusting your search or add new medications.
                </p>
            </div>

            <div v-else>
                <!-- Desktop Table View -->
                <div class="hidden md:block overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Product
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Category
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Stock
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Price
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Status
                                </th>
                                <th
                                    v-if="userRole === 'admin'"
                                    class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Actions
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr
                                v-for="medication in paginatedMedications"
                                :key="medication.id"
                                class="hover:bg-gray-50 transition-colors"
                            >
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="flex items-center">
                                        <div class="h-12 w-12 flex-shrink-0">
                                            <img
                                                v-if="
                                                    medication.images?.[0]
                                                        ?.image
                                                "
                                                :src="`https://techrems.pythonanywhere.com${medication.images[0].image}`"
                                                :alt="medication.name"
                                                class="h-12 w-12 rounded-lg object-cover border border-gray-200"
                                            />
                                            <div
                                                v-else
                                                class="h-12 w-12 rounded-lg bg-gray-100 flex items-center justify-center"
                                            >
                                                <Pill
                                                    class="w-6 h-6 text-gray-400"
                                                />
                                            </div>
                                        </div>
                                        <div class="ml-4">
                                            <div
                                                class="text-sm font-medium text-gray-900"
                                            >
                                                {{ medication.name }}
                                            </div>
                                            <div class="text-sm text-gray-500">
                                                {{
                                                    medication.description ||
                                                    "No description"
                                                }}
                                            </div>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span
                                        class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full"
                                    >
                                        {{
                                            medication.category?.name ||
                                            "Uncategorized"
                                        }}
                                    </span>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="flex items-center">
                                        <span
                                            :class="[
                                                'text-sm font-medium',
                                                medication.stock < 10
                                                    ? 'text-red-600'
                                                    : medication.stock < 20
                                                    ? 'text-yellow-600'
                                                    : 'text-green-600',
                                            ]"
                                        >
                                            {{ medication.stock }}
                                        </span>
                                        <span class="text-xs text-gray-500 ml-1"
                                            >units</span
                                        >
                                    </div>
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    ₵{{
                                        parseFloat(
                                            medication.price || 0
                                        ).toFixed(2)
                                    }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span
                                        :class="[
                                            'px-2 py-1 text-xs font-medium rounded-full',
                                            medication.stock > 20
                                                ? 'bg-green-100 text-green-800'
                                                : medication.stock > 0
                                                ? 'bg-yellow-100 text-yellow-800'
                                                : 'bg-red-100 text-red-800',
                                        ]"
                                    >
                                        {{
                                            medication.stock > 20
                                                ? "In Stock"
                                                : medication.stock > 0
                                                ? "Low Stock"
                                                : "Out of Stock"
                                        }}
                                    </span>
                                </td>
                                <td
                                    v-if="userRole === 'admin'"
                                    class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
                                >
                                    <div
                                        class="flex items-center justify-end gap-2"
                                    >
                                        <button
                                            @click="editMedication(medication)"
                                            class="text-orange-600 hover:text-orange-700 p-1 rounded"
                                        >
                                            <Edit class="w-4 h-4" />
                                        </button>
                                        <button
                                            @click="
                                                deleteMedication(medication.id)
                                            "
                                            class="text-red-600 hover:text-red-700 p-1 rounded"
                                        >
                                            <Trash2 class="w-4 h-4" />
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Mobile Card View -->
                <div class="md:hidden space-y-3">
                    <div
                        v-for="medication in paginatedMedications"
                        :key="medication.id"
                        class="bg-white border border-gray-200 rounded-lg p-2 shadow-sm"
                    >
                        <div class="flex items-start gap-2">
                            <div class="h-12 w-12 flex-shrink-0">
                                <img
                                    v-if="medication.images?.[0]?.image"
                                    :src="`https://techrems.pythonanywhere.com${medication.images[0].image}`"
                                    :alt="medication.name"
                                    class="h-12 w-12 rounded-lg object-cover border border-gray-200"
                                />
                                <div
                                    v-else
                                    class="h-12 w-12 rounded-lg bg-gray-100 flex items-center justify-center"
                                >
                                    <Pill class="w-6 h-6 text-gray-400" />
                                </div>
                            </div>

                            <div class="flex-1 min-w-0">
                                <h3
                                    class="text-sm font-medium text-gray-900 truncate"
                                >
                                    {{ medication.name }}
                                </h3>
                                <p class="text-xs text-gray-500 mt-1">
                                    {{
                                        medication.category?.name ||
                                        "Uncategorized"
                                    }}
                                </p>

                                <div
                                    class="flex items-center justify-between mt-3"
                                >
                                    <div class="flex items-center gap-4">
                                        <span
                                            class="text-sm font-medium text-gray-900"
                                            >₵{{
                                                parseFloat(
                                                    medication.price || 0
                                                ).toFixed(2)
                                            }}</span
                                        >
                                        <span
                                            :class="[
                                                'text-xs font-medium',
                                                medication.stock_quantity < 10
                                                    ? 'text-red-600'
                                                    : medication.stock_quantity <
                                                      20
                                                    ? 'text-yellow-600'
                                                    : 'text-green-600',
                                            ]"
                                        >
                                            {{ medication.stock_quantity }}
                                            units
                                        </span>
                                    </div>

                                    <div
                                        v-if="userRole === 'admin'"
                                        class="flex items-center gap-2"
                                    >
                                        <button
                                            @click="editMedication(medication)"
                                            class="text-orange-600 hover:text-orange-700 p-1 rounded"
                                        >
                                            <Edit class="w-4 h-4" />
                                        </button>
                                        <button
                                            @click="
                                                deleteMedication(medication.id)
                                            "
                                            class="text-red-600 hover:text-red-700 p-1 rounded"
                                        >
                                            <Trash2 class="w-4 h-4" />
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Pagination -->
                <div
                    v-if="totalPages > 1"
                    class="flex items-center justify-between mt-6"
                >
                    <div class="text-sm text-gray-500">
                        Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to
                        {{
                            Math.min(
                                currentPage * itemsPerPage,
                                filteredMedications.length
                            )
                        }}
                        of {{ filteredMedications.length }} medications
                    </div>

                    <div class="flex items-center gap-2">
                        <BaseButton
                            variant="outline"
                            size="sm"
                            :disabled="currentPage === 1"
                            @click="currentPage--"
                        >
                            <ChevronLeft class="w-4 h-4" />
                        </BaseButton>

                        <span
                            class="px-3 py-1 text-sm bg-orange-100 text-orange-700 rounded-lg"
                        >
                            {{ currentPage }} of {{ totalPages }}
                        </span>

                        <BaseButton
                            variant="outline"
                            size="sm"
                            :disabled="currentPage === totalPages"
                            @click="currentPage++"
                        >
                            <ChevronRight class="w-4 h-4" />
                        </BaseButton>
                    </div>
                </div>
            </div>
        </BaseCard>

        <!-- Add/Edit Modal -->
        <MedicationModal
            v-if="showAddModal || editingMedication"
            :medication="editingMedication"
            @close="closeModal"
            @saved="handleMedicationSaved"
        />
    </div>
</template>
