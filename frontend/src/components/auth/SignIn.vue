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
    <div class="lg:flex lg:h-screen lg:w-screen">
        <div
            class="w-screen min-h-screen flex justify-center items-center lg:w-1/2"
        >
            <form
                @submit.prevent="login"
                method="post"
                class="max-w-[370px] p-4 shadow w-11/12 mx-auto"
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
                <p class="mt-3 text-sm text-gray-700 text-">
                    Don't have an account?
                    <router-link to="/register" class="text-orange-700 text-xs"
                        >Sign up</router-link
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
