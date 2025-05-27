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

            // <-- Add this to refresh staff list -->
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
    <div class="h-screen w-full relative flex flex-col flex-1 overflow-hidden">
        <!-- Top Bar -->
        <div
            class="hidden w-full md:absolute top-0 z-40 bg-gray-900 shadow-md md:flex justify-between items-center p-3"
        >
            <h1 class="text-gray-300 font-styleScript text-lg md:text-2xl">
                Staff Hub
            </h1>
            <button
                @click="showModal = true"
                class="py-2 px-4 bg-orange-600 text-sm text-white font-medium hover:bg-orange-500"
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
                    class="py-2 px-4 bg-orange-600 text-sm text-white font-medium hover:bg-orange-500 md:hidden"
                >
                    Add Staff
                </button>

                <!-- Staff Table -->
                <div
                    class="max-h-[80vh] overflow-x-auto overscroll-contain mt-2 md:mt-14 mx-auto"
                >
                    <table
                        class="w-full text-sm text-left text-gray-700 bg-white shadow"
                    >
                        <thead
                            class="text-xs uppercase bg-gray-600 text-gray-800"
                        >
                            <tr>
                                <th class="px-6 py-3 whitespace-nowrap">
                                    Name
                                </th>
                                <th class="px-6 py-3 whitespace-nowrap">
                                    Email
                                </th>
                                <th class="px-6 py-3 whitespace-nowrap">
                                    Phone
                                </th>
                                <th
                                    class="px-6 py-3 whitespace-nowrap text-center"
                                >
                                    Update
                                </th>
                                <th
                                    class="px-6 py-3 whitespace-nowrap text-center"
                                >
                                    Delete
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="staff in staffList"
                                :key="staff.id"
                                class="border-b hover:bg-gray-200"
                            >
                                <td class="px-6 py-4 whitespace-nowrap">
                                    {{ staff.profile.first_name }}
                                    {{ staff.profile.last_name }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    {{ staff.email }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    {{ staff.profile.phone }}
                                </td>
                                <td class="px-6 py-4 text-center">
                                    <button class="text-blue-600 text-2xl">
                                        <i class="pi pi-user-edit"></i>
                                    </button>
                                </td>
                                <td class="px-6 py-4 text-center">
                                    <button
                                        @click="deleteStaff(staff.id)"
                                        class="text-red-600 text-2xl"
                                        title="Delete staff"
                                    >
                                        <i class="pi pi-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Modal -->
                <div
                    v-if="showModal"
                    class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
                >
                    <div class="w-full p-3">
                        <form
                            @submit.prevent="submitStaff"
                            class="w-full max-w-xl max-h-[90vh] overflow-y-auto p-4 shadow mx-auto bg-white rounded"
                        >
                            <div class="flex justify-between items-center mb-4">
                                <h1 class="text-lg font-bold text-gray-800">
                                    Register Staff
                                </h1>
                                <button
                                    type="button"
                                    @click="showModal = false"
                                    class="text-orange-600 text-xl"
                                >
                                    <i class="pi pi-times"></i>
                                </button>
                            </div>

                            <!-- Row 1 -->
                            <div class="md:flex gap-4">
                                <InputField
                                    v-model="form.first_name"
                                    labelname="First Name"
                                    class="flex-1"
                                />
                                <InputField
                                    v-model="form.last_name"
                                    labelname="Last Name"
                                    class="flex-1"
                                />
                            </div>

                            <!-- Row 2 -->
                            <div class="md:flex gap-4 mt-3">
                                <label
                                    class="flex-1 text-sm text-gray-900 block mt-3"
                                >
                                    Other Names
                                    <input
                                        v-model="form.other_names"
                                        type="text"
                                        class="block mt-1 w-full border border-gray-400 rounded outline-none focus:border-orange-700 h-9 px-4 md:h-10 bg-transparent"
                                        required
                                    />
                                </label>
                                <InputField
                                    v-model="form.address"
                                    labelname="Address"
                                    class="flex-1"
                                />
                            </div>

                            <!-- Row 3 -->
                            <div class="md:flex gap-4 mt-3">
                                <InputField
                                    v-model="form.phone"
                                    labelname="Phone"
                                    type="tel"
                                    class="flex-1"
                                />
                                <InputField
                                    v-model="form.email"
                                    labelname="Email"
                                    type="email"
                                    class="flex-1"
                                />
                            </div>

                            <!-- Submit Button -->
                            <div class="mt-5">
                                <Btn :disabled="isSubmitting" btnName="Save" />
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
