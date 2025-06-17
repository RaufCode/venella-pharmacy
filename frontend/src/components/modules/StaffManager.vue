<script setup>
    import { ref, computed, onMounted } from "vue";
    import {
        Plus,
        Users,
        UserCheck,
        UserPlus,
        Edit,
        Trash2,
    } from "lucide-vue-next";
    import { useToast } from "vue-toastification";

    import BaseCard from "@/components/shared/BaseCard.vue";
    import BaseButton from "@/components/shared/BaseButton.vue";
    import StaffModal from "@/components/modals/StaffModal.vue";

    import axios from "axios";

    const toast = useToast();

    const staffList = ref([]);
    const isLoading = ref(false);
    const showAddModal = ref(false);
    const editingStaff = ref(null);

    const activeStaffCount = computed(() => staffList.value.length); // Assuming all are active for now

    const newStaffThisMonth = computed(() => {
        const thisMonth = new Date().getMonth();
        const thisYear = new Date().getFullYear();

        return staffList.value.filter((staff) => {
            const joinDate = new Date(staff.date_joined);
            return (
                joinDate.getMonth() === thisMonth &&
                joinDate.getFullYear() === thisYear
            );
        }).length;
    });

    const fetchStaff = async () => {
        try {
            isLoading.value = true;
            const response = await axios.get(
                "/api/core/accounts/salespersons/"
            );
            staffList.value = response.data;
        } catch (error) {
            toast.error("Failed to fetch staff.");
        } finally {
            isLoading.value = false;
        }
    };

    const editStaff = (staff) => {
        editingStaff.value = staff;
    };

    const deleteStaff = async (id) => {
        if (!confirm("Are you sure you want to delete this staff member?")) {
            return;
        }
        try {
            await axios.delete(`/api/core/accounts/${id}/delete/`);
            await fetchStaff();
            toast.success("Staff deleted successfully.");
        } catch (error) {
            toast.error("Failed to delete staff.");
        }
    };

    const closeModal = () => {
        showAddModal.value = false;
        editingStaff.value = null;
    };

    const handleStaffSaved = () => {
        closeModal();
        fetchStaff();
    };

    const getInitials = (firstName, lastName) => {
        return `${firstName?.charAt(0) || ""}${
            lastName?.charAt(0) || ""
        }`.toUpperCase();
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString();
    };

    onMounted(() => {
        fetchStaff();
    });
</script>
<template>
    <div class="space-y-6">
        <!-- Header -->
        <div
            class="flex flex-col lg:flex-row lg:items-center justify-between gap-4"
        >
            <div>
                <h2 class="text-xl font-semibold text-gray-900">
                    Staff Management
                </h2>
                <p class="text-sm text-gray-600">
                    Manage salesperson accounts and permissions
                </p>
            </div>

            <BaseButton @click="showAddModal = true">
                <template #icon>
                    <Plus class="w-4 h-4" />
                </template>
                Add Staff Member
            </BaseButton>
        </div>

        <!-- Staff Stats -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div class="bg-white rounded-lg border border-gray-200 p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-600">Total Staff</p>
                        <p class="text-2xl font-semibold text-gray-900 mt-1">
                            {{ staffList.length }}
                        </p>
                    </div>
                    <div
                        class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center"
                    >
                        <Users class="w-5 h-5 text-blue-600" />
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg border border-gray-200 p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-600">Active Staff</p>
                        <p class="text-2xl font-semibold text-gray-900 mt-1">
                            {{ activeStaffCount }}
                        </p>
                    </div>
                    <div
                        class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center"
                    >
                        <UserCheck class="w-5 h-5 text-green-600" />
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg border border-gray-200 p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm text-gray-600">This Month</p>
                        <p class="text-2xl font-semibold text-gray-900 mt-1">
                            {{ newStaffThisMonth }}
                        </p>
                    </div>
                    <div
                        class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center"
                    >
                        <UserPlus class="w-5 h-5 text-purple-600" />
                    </div>
                </div>
            </div>
        </div>

        <!-- Staff List -->
        <BaseCard title="Staff Members" subtitle="Manage your pharmacy staff">
            <div
                v-if="isLoading"
                class="flex items-center justify-center py-12"
            >
                <div
                    class="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"
                ></div>
            </div>

            <div v-else-if="staffList.length === 0" class="text-center py-12">
                <Users class="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <h3 class="text-lg font-medium text-gray-900">
                    No staff members
                </h3>
                <p class="text-gray-500">
                    Add your first staff member to get started.
                </p>
            </div>

            <div v-else>
                <!-- Desktop Table -->
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Email
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Role
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Status
                                </th>
                                <th
                                    class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Actions
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr
                                v-for="staff in staffList"
                                :key="staff.id"
                                class="hover:bg-gray-50 transition-colors"
                            >
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="text-sm text-gray-900">
                                        {{ staff.email }}
                                    </div>
                                    <div class="text-sm text-gray-500">
                                        {{ staff.phone }}
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span
                                        class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full"
                                    >
                                        Salesperson
                                    </span>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span
                                        class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full"
                                    >
                                        Active
                                    </span>
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
                                >
                                    <div
                                        class="flex items-center justify-end gap-2"
                                    >
                                        <button
                                            @click="editStaff(staff)"
                                            class="text-orange-600 hover:text-orange-700 p-1 rounded"
                                        >
                                            <Edit class="w-4 h-4" />
                                        </button>
                                        <button
                                            @click="deleteStaff(staff.id)"
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

                <!-- Mobile Cards
                <div class="md:hidden space-y-4">
                    <div
                        v-for="staff in staffList"
                        :key="staff.id"
                        class="bg-white border border-gray-200 rounded-lg p-4 shadow-sm"
                    >
                        <div class="flex items-start gap-3">
                            <div class="h-12 w-12 flex-shrink-0">
                                <div
                                    class="h-12 w-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center"
                                >
                                    <span
                                        class="text-white font-semibold text-sm"
                                    >
                                        {{
                                            getInitials(
                                                staff.first_name,
                                                staff.last_name
                                            )
                                        }}
                                    </span>
                                </div>
                            </div>

                            <div class="flex-1 min-w-0">
                                <h3 class="text-sm font-medium text-gray-900">
                                    {{ staff.first_name }} {{ staff.last_name }}
                                </h3>
                                <p class="text-xs text-gray-500 mt-1">
                                    {{ staff.email }}
                                </p>
                                <p class="text-xs text-gray-500">
                                    {{ staff.phone }}
                                </p>

                                <div class="flex items-center gap-2 mt-3">
                                    <span
                                        class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full"
                                    >
                                        Salesperson
                                    </span>
                                    <span
                                        class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full"
                                    >
                                        Active
                                    </span>
                                </div>

                                <div
                                    class="flex items-center justify-between mt-4"
                                >
                                    <span class="text-xs text-gray-500">
                                        Added
                                        {{ formatDate(staff.date_joined) }}
                                    </span>

                                    <div class="flex items-center gap-2">
                                        <button
                                            @click="editStaff(staff)"
                                            class="text-orange-600 hover:text-orange-700 p-1 rounded"
                                        >
                                            <Edit class="w-4 h-4" />
                                        </button>
                                        <button
                                            @click="deleteStaff(staff.id)"
                                            class="text-red-600 hover:text-red-700 p-1 rounded"
                                        >
                                            <Trash2 class="w-4 h-4" />
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div> -->
            </div>
        </BaseCard>

        <!-- Add/Edit Staff Modal -->
        <StaffModal
            v-if="showAddModal || editingStaff"
            :staff="editingStaff"
            @close="closeModal"
            @saved="handleStaffSaved"
        />
    </div>
</template>
