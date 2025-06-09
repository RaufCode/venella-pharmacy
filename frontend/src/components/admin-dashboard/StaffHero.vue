<script setup>
    import { ref, reactive, watch, onMounted } from "vue";
    import axios from "axios";
    import InputField from "@/components/ui/InputField.vue";
    import Btn from "@/components/ui/Btn.vue";
    import { useAuthStore } from "@/stores/auth";

    const authStore = useAuthStore();

    const showModal = ref(false);
    const isSubmitting = ref(false);

    const staffList = ref([]);

    // Fetch salespersons from API
    const fetchStaff = async () => {
        try {
            const response = await axios.get(
                "/api/core/accounts/salespersons/"
            );
            staffList.value = response.data;
            console.log(staffList.value);
        } catch (error) {
            console.error("Failed to fetch staff:", error);
        }
    };

    // Fetch staff when component is mounted
    onMounted(() => {
        fetchStaff();
    });

    const form = reactive({
        first_name: "",
        last_name: "",
        other_names: "",
        email: "",
        phone: "",
        address: "",
    });

    const formatName = (name) => {
        if (!name) return "";
        return name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();
    };

    const resetForm = () => {
        for (const key in form) {
            form[key] = "";
        }
    };

    watch(showModal, (newVal, oldVal) => {
        if (oldVal === true && newVal === false) {
            resetForm();
        }
    });

    const submitStaff = async () => {
        if (isSubmitting.value) return;
        isSubmitting.value = true;

        try {
            // Format names
            form.first_name = formatName(form.first_name.trim());
            form.last_name = formatName(form.last_name.trim());
            form.other_names = formatName(form.other_names.trim());
            form.email = form.email.trim().toLowerCase();

            // Normalize phone number
            if (form.phone.startsWith("0")) {
                form.phone = "+233" + form.phone.slice(1);
            }

            const payload = {
                first_name: form.first_name,
                last_name: form.last_name,
                other_names: form.other_names,
                email: form.email,
                phone: form.phone,
                address: form.address,
            };

            await axios.post(
                "/api/core/accounts/salesperson/create/",
                payload,
                {
                    headers: {
                        Authorization: `Bearer ${authStore.token}`,
                        "Content-Type": "application/json",
                    },
                }
            );

            alert("Staff added successfully!");

            // Refresh staff list
            await fetchStaff();

            showModal.value = false;
            resetForm();
        } catch (error) {
            const errData = error.response?.data;
            console.error("Error:", errData || error.message);

            if (errData?.errors) {
                const messages = Object.entries(errData.errors)
                    .map(([field, msgs]) => `${field}: ${msgs.join(", ")}`)
                    .join("\n");
                alert(`Failed to add staff:\n${messages}`);
            } else {
                alert(errData?.detail || "Submission failed.");
            }
        } finally {
            isSubmitting.value = false;
        }
    };

    const deleteStaff = async (userId) => {
        if (!confirm("Are you sure you want to delete this staff member?"))
            return;

        try {
            await axios.delete(
                `/api/core/accounts/salesperson/${userId}/remove/`,
                {
                    headers: {
                        Authorization: `Bearer ${authStore.token}`,
                    },
                }
            );

            // Remove the deleted staff from local staffList immediately
            staffList.value = staffList.value.filter(
                (staff) => staff.id !== userId
            );

            alert("Staff member deleted successfully.");
        } catch (error) {
            console.error("Failed to delete staff:", error);
            alert(
                error.response?.data?.detail ||
                    "An error occurred while deleting staff."
            );
        }
    };
</script>

<template>
    <div class="h-screen w-full relative flex flex-col">
        <!-- Top Bar -->
        <div
            class="hidden md:flex justify-between items-center bg-white w-full p-4 shadow static top-0 z-50"
        >
            <h1 class="text-gray-700 font-styleScript text-3xl">Staff Hub</h1>
            <button
                @click="showModal = true"
                class="py-2 px-4 rounded-lg bg-orange-600 text-sm text-white font-medium hover:bg-orange-500"
            >
                Add Staff
            </button>
        </div>

        <!-- Main Content -->
        <div class="overflow-y-auto overscroll-contain w-full">
            <div class="mx-auto container p-3">
                <!-- Button (Mobile) -->
                <button
                    @click="showModal = true"
                    class="py-2 px-4 mt-4 rounded-lg bg-orange-600 text-sm text-white font-medium hover:bg-orange-500 md:hidden"
                >
                    Add Staff
                </button>

                <!-- Staff Table -->
                <div
                    class="overflow-x-auto overscroll-contain mt-2 md:mt-0 mx-auto bg-white"
                >
                    <table
                        v-if="staffList.length > 0"
                        class="min-w-full divide-y divide-gray-200 table-auto"
                    >
                        <thead class="bg-gray-200 text-gray-600 text-sm">
                            <tr>
                                <th
                                    class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider truncate"
                                    scope="col"
                                >
                                    Name
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider truncate"
                                    scope="col"
                                >
                                    Email
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider truncate"
                                    scope="col"
                                >
                                    Phone
                                </th>
                                <th
                                    class="px-6 py-3 text-center text-xs font-semibold uppercase tracking-wider"
                                    scope="col"
                                >
                                    Update
                                </th>
                                <th
                                    class="px-6 py-3 text-center text-xs font-semibold uppercase tracking-wider"
                                    scope="col"
                                >
                                    Delete
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr
                                v-for="staff in staffList"
                                :key="staff.id"
                                class="hover:bg-gray-50 hover:shadow-lg transition-colors duration-150 cursor-pointer"
                                :title="`${staff.profile.first_name} ${staff.profile.last_name}`"
                            >
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900 truncate max-w-xs"
                                >
                                    {{ staff.profile.first_name }}
                                    {{ staff.profile.last_name }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-indigo-600 truncate max-w-md"
                                >
                                    {{ staff.email }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-orange-600 truncate max-w-xs"
                                >
                                    {{ staff.profile.phone }}
                                </td>
                                <td class="px-6 py-4 text-center">
                                    <button
                                        class="text-blue-600 hover:text-blue-800 text-xl transition"
                                        title="Edit staff"
                                        aria-label="Edit staff"
                                    >
                                        <i class="pi pi-user-edit"></i>
                                    </button>
                                </td>
                                <td class="px-6 py-4 text-center">
                                    <button
                                        @click="deleteStaff(staff.id)"
                                        class="text-red-600 hover:text-red-800 text-xl transition"
                                        title="Delete staff"
                                        aria-label="Delete staff"
                                    >
                                        <i class="pi pi-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <div
                        v-if="staffList.length === 0"
                        class="text-center text-gray-500 mt-10 py-16"
                    >
                        <p>
                            <i
                                class="pi pi-user text-3xl md:text-5xl animate-pulse"
                            ></i>
                        </p>
                        <p>No staff members found</p>
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
                        <form @submit.prevent="submitStaff" class="space-y-6">
                            <div class="flex justify-between items-center">
                                <h2 class="text-xl font-bold text-gray-800">
                                    Register Staff
                                </h2>
                                <button
                                    type="button"
                                    @click="showModal = false"
                                    class="text-orange-600 text-2xl hover:text-orange-800 transition"
                                    aria-label="Close modal"
                                >
                                    <i class="pi pi-times"></i>
                                </button>
                            </div>

                            <!-- Name inputs -->
                            <div class="md:flex gap-4">
                                <InputField
                                    v-model="form.first_name"
                                    labelname="First Name"
                                    class="flex-1"
                                    required
                                />
                                <InputField
                                    v-model="form.last_name"
                                    labelname="Last Name"
                                    class="flex-1"
                                    required
                                />
                            </div>

                            <!-- Other Names & Address -->
                            <div class="md:flex gap-4">
                                <label
                                    class="flex-1 block mt-3 text-sm text-gray-900"
                                >
                                    Other Names
                                    <input
                                        v-model="form.other_names"
                                        type="text"
                                        class="mt-1 w-full border border-gray-400 rounded px-4 py-2 focus:outline-none focus:border-orange-700 bg-transparent"
                                    />
                                </label>
                                <InputField
                                    v-model="form.address"
                                    labelname="Address"
                                    class="flex-1"
                                    required
                                />
                            </div>

                            <!-- Phone & Email -->
                            <div class="md:flex gap-4">
                                <InputField
                                    v-model="form.phone"
                                    labelname="Phone"
                                    type="tel"
                                    class="flex-1"
                                    required
                                />
                                <InputField
                                    v-model="form.email"
                                    labelname="Email"
                                    type="email"
                                    class="flex-1"
                                    required
                                />
                            </div>

                            <!-- Submit Button -->
                            <div>
                                <Btn :disabled="isSubmitting" btnName="Save" />
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
