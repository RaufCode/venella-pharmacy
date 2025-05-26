<script setup>
    import InputField from "@/components/ui/InputField.vue";
    import Btn from "@/components/ui/Btn.vue";
    import { ref, reactive } from "vue";
    import { useAuthStore } from "@/stores/auth"; // Import Pinia store
    import { useRouter } from "vue-router"; // Import router

    const authStore = useAuthStore(); // Initialize auth store
    const router = useRouter(); // Initialize router// Initialize auth store

    const form = reactive({
        first_name: "",
        last_name: "",
        other_names: "",
        email: "",
        phone: "",
        address: "",
        password: "",
        role: "",
    });

    const validation = async () => {
        form.first_name =
            form.first_name.charAt(0).toUpperCase() +
            form.first_name.slice(1).toLowerCase();
        form.last_name =
            form.last_name.charAt(0).toUpperCase() +
            form.last_name.slice(1).toLowerCase();
        form.other_names =
            form.other_names.charAt(0).toUpperCase() +
            form.other_names.slice(1).toLowerCase();
        form.email = form.email.toLowerCase();
        console.log(form);
        if (form.phone.startsWith("0")) {
            form.phone = "+233" + form.phone.slice(1);
        }

        try {
            await authStore.register(form); // Call the store's register action
        } catch (error) {
            console.error("Registration failed:", error.message);
        }
    };
</script>

<template>
    <div class="p-3 md:p-0 bg-gray-100">
        <div class="flex items-center min-h-screen w-full">
            <form
                @submit.prevent="validation"
                class="w-full max-w-xl p-3 md:p-4 shadow mx-auto bg-white rounded"
            >
                <h1 class="form-title text-center">Register Here</h1>
                <div class="md:flex items-center flex-col md:flex-row gap-4">
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
                <div
                    class="md:flex items-center flex-col md:flex-row gap-4 mt-3 md:mt-0"
                >
                    <label class="flex-1 text-sm text-gray-900 mt-3">
                        Other Names
                        <input
                            v-model="form.other_names"
                            type="text"
                            class="block mt-1 w-full border border-gray-400 rounded outline-none focus:border-orange-700 h-9 px-4 md:h-10 bg-transparent"
                        />
                    </label>
                    <InputField
                        v-model="form.email"
                        labelname="Email"
                        type="email"
                        class="flex-1"
                    />
                </div>
                <div class="md:flex items-center flex-col md:flex-row gap-4">
                    <InputField
                        v-model="form.phone"
                        labelname="Phone"
                        type="tel"
                        class="flex-1"
                    />
                    <InputField
                        v-model="form.address"
                        labelname="Address"
                        class="flex-1"
                    />
                </div>
                <div class="mt-3">
                    <label for="role" class="block text-sm text-gray-900"
                        >Role</label
                    >
                    <select
                        id="role"
                        v-model="form.role"
                        required
                        class="block mt-1 w-full border text-sm text-gray-700 bg-inherit border-gray-400 rounded outline-none focus:border-orange-700 h-9 p-1 md:h-10"
                    >
                        <option value="" disabled>Select Role</option>
                        <option value="customer">Customer</option>
                    </select>
                </div>
                <InputField
                    v-model="form.password"
                    labelname="Password"
                    type="password"
                    class="mt-3"
                />
                <Btn btnName="Sign up" class="mt-4" />
                <p class="mt-3 text-sm text-gray-700 text-center">
                    Already have an account?
                    <router-link to="/login" class="text-orange-700 text-xs"
                        >Sign in</router-link
                    >
                </p>
            </form>
        </div>
    </div>
</template>
