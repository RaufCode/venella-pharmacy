<script setup>
    import { ref } from "vue";
    import InputField from "@/components/ui/InputField.vue";
    import Btn from "@/components/ui/Btn.vue";
    const showModal = ref(false);
    const staffList = ref([
        {
            name: "Jane Smith",
            email: "jane.smith@gmail.com",
            role: "Cashier",
            image: "https://i.pravatar.cc/100?img=5",
            phone: "+233 123 456 789",
        },
        {
            name: "John Doe",
            email: "john.doe@gmail.com",
            role: "Pharmacist",
            image: "https://i.pravatar.cc/100?img=2",
            phone: "+233 234 567 890",
        },
        {
            name: "John Doe",
            email: "john.doe@gmail.com",
            role: "Pharmacist",
            image: "https://i.pravatar.cc/100?img=2",
            phone: "+233 345 678 901",
        },
        {
            name: "Jane Smith",
            email: "jane.smith@gmail.com",
            role: "Cashier",
            image: "https://i.pravatar.cc/100?img=5",
            phone: "+233 456 789 012",
        },
        {
            name: "Linda Johnson",
            email: "linda.johnson@gmail.com",
            role: "Assistant",
            image: "https://i.pravatar.cc/100?img=10",
            phone: "+233 567 890 123",
        },
        {
            name: "Michael Brown",
            email: "michael.brown@gmail.com",
            role: "Manager",
            image: "https://i.pravatar.cc/100?img=15",
            phone: "+233 678 901 234",
        },
    ]);

    const isEditing = ref(false);
    const currentEditIndex = ref(null);

    const form = ref({
        name: "",
        role: "",
    });

    function openAddModal() {
        form.value = { name: "", role: "" };
        isEditing.value = false;
        showModal.value = true;
    }

    function openEditModal(index) {
        form.value = { ...staffList.value[index] };
        currentEditIndex.value = index;
        isEditing.value = true;
        showModal.value = true;
    }

    function closeModal() {
        showModal.value = false;
    }

    function saveStaff() {
        if (isEditing.value) {
            staffList.value[currentEditIndex.value] = { ...form.value };
        } else {
            staffList.value.push({ ...form.value });
        }
        closeModal();
    }

    function deleteStaff(index) {
        if (confirm("Are you sure you want to delete this staff member?")) {
            staffList.value.splice(index, 1);
        }
    }
</script>

<template>
    <div class="h-screen w-full relative flex flex-col flex-1 overflow-hidden">
        <div
            class="hidden w-full md:absolute top-0 z-40 bg-gray-900 shadow-md md:flex justify-between items-center p-3"
        >
            <h1
                class="text-gray-300 font-styleScript text-center text-lg md:text-2xl"
            >
                Staff Hub
            </h1>
            <button
                @click="showModal = true"
                type="submit"
                class="py-2 px-4 bg-orange-600 text-sm text-white font-medium hover:bg-orange-500"
            >
                Add Staff
            </button>
        </div>
        <div class="overflow-y-auto overscroll-contain w-full">
            <div class="mx-auto container p-3">
                <button
                    @click="showModal = true"
                    type="submit"
                    class="py-2 px-4 bg-orange-600 text-sm text-white font-medium hover:bg-orange-500"
                >
                    Add Staff
                </button>
                <div
                    class="lg:min-w-full max-h-[80vh] overflow-x-auto overscroll-contain mt-2 md:mt-5 mx-auto"
                >
                    <table
                        class="w-full text-sm text-left text-gray-700 bg-white shadow"
                    >
                        <thead
                            class="text-xs uppercase bg-gray-600 text-gray-800"
                        >
                            <tr>
                                <th class="px-6 py-3">Image</th>
                                <th class="px-6 py-3">Name</th>
                                <th class="px-6 py-3">Email</th>
                                <th class="px-6 py-3">Phone</th>
                                <th class="px-6 py-3">Role</th>
                                <th class="px-6 py-3">Update</th>
                                <th class="px-6 py-3">Delete</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="(staff, index) in staffList"
                                :key="index"
                                class="border-b hover:bg-gray-200"
                            >
                                <td class="">
                                    <img
                                        :src="staff.image"
                                        class="w-full h-full object-cover"
                                        alt="Staff Image"
                                    />
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    {{ staff.name }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    {{ staff.email }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    {{ staff.phone }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    {{ staff.role }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <button
                                        class="text-white px-3 py-1"
                                        @click="openEditModal(index)"
                                    >
                                        <i
                                            class="pi pi-user-edit text-blue-600 text-2xl"
                                        ></i>
                                    </button>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <button
                                        class="text-white px-3 py-1"
                                        @click="deleteStaff(index)"
                                    >
                                        <i
                                            class="pi pi-trash text-red-600 text-2xl"
                                        ></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Add Staff Modal -->
                <div
                    v-if="showModal"
                    class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
                >
                    <div
                        class="bg-white overflow-hidden shadow w-11/12 max-w-md max-h-[70vh] p-5 overflow-y-auto"
                    >
                        <form class="w-full">
                            <!-- Modal Header -->
                            <div class="flex justify-between items-center">
                                <h1 class="form-title">Add Staff</h1>
                                <p
                                    @click="showModal = false"
                                    class="cursor-pointer"
                                >
                                    <i class="pi pi-times text-orange-600"></i>
                                </p>
                            </div>

                            <!-- Staff Form Fields -->
                            <InputField
                                labelname="Full Name"
                                type="text"
                                v-model="form.name"
                            />
                            <InputField
                                labelname="Email Address"
                                type="email"
                                v-model="form.email"
                            />
                            <InputField
                                labelname="Password"
                                type="password"
                                v-model="form.email"
                            />
                            <InputField
                                labelname="Phone Number"
                                type="text"
                                v-model="form.phone"
                            />

                            <!-- Role Selection -->
                            <label
                                class="block mx-auto mt-3 text-sm text-gray-900"
                            >
                                Role
                                <select
                                    v-model="form.role"
                                    class="block mt-1 w-full mx-auto border border-gray-400 rounded outline-none focus:border-orange-700 h-9 p-1 md:h-10 bg-transparent"
                                >
                                    <option value="" disabled>
                                        Select Role
                                    </option>
                                    <option value="Pharmacist">
                                        Pharmacist
                                    </option>
                                    <option value="Cashier">Cashier</option>
                                    <option value="Manager">Manager</option>
                                    <option value="Assistant">Assistant</option>
                                    <option value="Delivery Staff">
                                        Delivery Staff
                                    </option>
                                    <option value="Technician">
                                        Technician
                                    </option>
                                </select>
                            </label>

                            <!-- Staff Image Upload (Optional) -->
                            <label
                                class="block mx-auto mt-3 text-sm text-gray-900"
                            >
                                Staff Image (optional)
                                <input
                                    type="file"
                                    class="block mt-1 w-full mx-auto border border-gray-400 rounded outline-none focus:border-orange-700 h-9 p-1 md:h-10 bg-transparent"
                                />
                            </label>

                            <!-- Save Button -->
                            <Btn btnName="Save" />
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
