<script setup>
    import InputField from "@/components/ui/InputField.vue";
    import Btn from "@/components/ui/Btn.vue"; // Fix casing issue in Btn import
    import { reactive } from "vue";
    import { useAuthStore } from "@/stores/auth"; // Import auth store
    import { useRouter } from "vue-router"; // Import Vue Router

    const authStore = useAuthStore(); // Initialize auth store
    const router = useRouter(); // Initialize router

    const form = reactive({
        email: "",
        password: "",
    });

    const login = async () => {
        form.email = form.email.toLowerCase();
        console.log(form); // Log form data
        try {
            await authStore.login(form); // Call the store's login action
        } catch (error) {
            console.error("Login failed:", error.message);
        }
    };
</script>
<template>
    <div class="">
        <div
            class="flex justify-center items-center h-screen p-3 md:p-0 bg-gray-100"
        >
            <form
                @submit.prevent="login"
                method="post"
                class="w-full max-w-lg p-3 md:p-4 shadow mx-auto bg-white rounded"
            >
                <h1 class="form-title">Sign in</h1>
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
                <Btn btnName="Sign in" />
                <p class="mt-3 text-sm text-gray-700 text-center">
                    Don't have an account?
                    <router-link to="/register" class="text-orange-700 text-xs"
                        >Sign up</router-link
                    >
                </p>
            </form>
        </div>
    </div>
</template>
