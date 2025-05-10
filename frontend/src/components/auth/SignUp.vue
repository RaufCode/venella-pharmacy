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
        adress: "",
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
        try {
            await authStore.register(form); // Call the store's register action
        } catch (error) {
            console.error("Registration failed:", error.message);
        }
    };
</script>

<template>
    <div class="grid lg:grid-cols-2 lg:h-screen">
        <div
            class="overflow-y-scroll py-4 bg-white 2lg:flex 2lg:justify-center 2lg:items-center"
        >
            <form
                @submit.prevent="validation"
                class="max-w-[370px] p-3 shadow w-11/12 mx-auto"
            >
                <h1 class="form-title">Sign up</h1>
                <InputField v-model="form.first_name" labelname="First Name" />
                <InputField v-model="form.last_name" labelname="Last Name" />
                <label class="block mx-auto mt-3 text-sm text-gray-900">
                    Other Names
                    <input
                        v-model="form.other_names"
                        type="text"
                        class="block mt-1 w-full mx-auto border border-gray-400 rounded outline-none focus:border-orange-700 h-9 px-4 md:h-10 bg-transparent"
                    />
                </label>
                <InputField
                    v-model="form.email"
                    labelname="Email"
                    type="email"
                />
                <InputField v-model="form.phone" labelname="Phone" />
                <InputField v-model="form.adress" labelname="Address" />
                <div>
                    <label
                        for="role"
                        class="block mx-auto mt-3 text-sm text-gray-900"
                    >
                        Role
                    </label>
                    <select
                        id="role"
                        class="block mt-1 w-full mx-auto border text-sm text-gray-700 border-gray-400 rounded outline-none focus:border-orange-700 h-9 p-1 md:h-10"
                        v-model="form.role"
                        required
                    >
                        <option value="" disabled>Select Role</option>
                        <option value="customer">Customer</option>
                    </select>
                </div>
                <InputField
                    v-model="form.password"
                    labelname="Password"
                    type="password"
                />
                <Btn btnName="Sign up" />
                <p class="mt-3 text-sm text-gray-700">
                    Already have an account?
                    <router-link to="/login" class="text-orange-700 text-xs"
                        >Sign in</router-link
                    >
                </p>
            </form>
        </div>
        <div class="hidden lg:flex items-center justify-center bg-orange-700">
            <h1 class="text-5xl font-styleScript text-white">
                Venella Pharmacy
            </h1>
        </div>
    </div>
</template>
