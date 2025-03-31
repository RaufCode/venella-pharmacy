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
        email: "",
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

        if (form.role === "admin" && form.password !== "ven@pharmacy") {
            alert("you are not authorized to register as an admin");
            return;
        }
        console.log(form);
        try {
            await authStore.register(form); // Call the store's register action
        } catch (error) {
            console.error("Registration failed:", error.message);
        }
    };
</script>

<template>
    <div class="flex lg:h-screen lg:w-screen">
        <div
            class="w-screen min-h-screen flex justify-center items-center lg:w-1/2"
        >
            <form
                @submit.prevent="validation"
                class="max-w-[370px] p-5 shadow w-11/12 mx-auto"
            >
                <h1 class="form-title">Sign up</h1>
                <InputField v-model="form.first_name" labelname="First Name" />
                <InputField v-model="form.last_name" labelname="Last Name" />
                <InputField
                    v-model="form.email"
                    labelname="Email"
                    type="email"
                />
                <InputField
                    v-model="form.password"
                    labelname="Password"
                    type="password"
                />
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
                        <option value="admin">Admin</option>
                        <option value="customer">Customer</option>
                    </select>
                </div>
                <Btn btnName="Sign up" />
                <p class="mt-3 text-sm text-gray-700">
                    Already have an account?
                    <router-link to="/login" class="text-orange-700 text-xs"
                        >Sign in</router-link
                    >
                </p>
            </form>
        </div>
        <div
            class="hidden lg:flex items-center justify-center lg:w-1/2 lg:h-full bg-orange-700"
        >
            <h1 class="text-5xl font-styleScript text-white">
                Venella Pharmacy
            </h1>
        </div>
    </div>
</template>
