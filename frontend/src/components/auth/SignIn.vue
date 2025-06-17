<script setup>
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
    <div
        class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-orange-50 flex items-center justify-center p-4"
    >
        <div class="w-full max-w-md">
            <!-- Logo and Header -->
            <div class="text-center mb-8">
                <div
                    class="w-16 h-16 bg-gradient-to-br from-orange-500 to-red-600 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg"
                >
                    <span class="text-white font-bold text-xl">V</span>
                </div>
                <h1
                    class="text-3xl font-styleScript bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent mb-2"
                >
                    Welcome Back
                </h1>
                <p class="text-gray-600">Sign in to your VPharm account</p>
            </div>

            <!-- Sign In Form -->
            <div
                class="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden"
            >
                <div class="p-4 md:p-8">
                    <!-- Error Display -->
                    <div
                        v-if="authStore.error"
                        class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl"
                    >
                        <div class="flex items-start gap-3">
                            <svg
                                class="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16c-.77.833.192 2.5 1.732 2.5z"
                                ></path>
                            </svg>
                            <p class="text-red-700 text-sm">
                                {{ authStore.error }}
                            </p>
                        </div>
                    </div>

                    <form @submit.prevent="login" class="space-y-6">
                        <!-- Email Field -->
                        <div>
                            <label
                                class="block text-sm font-medium text-gray-700 mb-2"
                            >
                                Email Address
                            </label>
                            <div class="relative">
                                <input
                                    v-model="form.email"
                                    type="email"
                                    name="email"
                                    autocomplete="email"
                                    required
                                    :disabled="authStore.loading"
                                    class="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:border-orange-500 transition-all duration-200 disabled:bg-gray-100 disabled:cursor-not-allowed pl-12"
                                    placeholder="Enter email address"
                                />
                                <div
                                    class="absolute left-4 top-1/2 transform -translate-y-1/2"
                                >
                                    <svg
                                        class="w-5 h-5 text-gray-400"
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                                        ></path>
                                    </svg>
                                </div>
                            </div>
                        </div>

                        <!-- Password Field -->
                        <div>
                            <label
                                class="block text-sm font-medium text-gray-700 mb-2"
                            >
                                Password
                            </label>
                            <div class="relative">
                                <input
                                    v-model="form.password"
                                    type="password"
                                    name="password"
                                    autocomplete="current-password"
                                    required
                                    :disabled="authStore.loading"
                                    class="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:border-orange-500 transition-all duration-200 disabled:bg-gray-100 disabled:cursor-not-allowed pl-12"
                                    placeholder="Enter password"
                                />
                                <div
                                    class="absolute left-4 top-1/2 transform -translate-y-1/2"
                                >
                                    <svg
                                        class="w-5 h-5 text-gray-400"
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            stroke-width="2"
                                            d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                                        ></path>
                                    </svg>
                                </div>
                            </div>
                        </div>

                        <!-- Forgot Password Link -->
                        <div class="text-right">
                            <a
                                href="#"
                                class="text-sm text-orange-600 hover:text-orange-700 font-medium transition-colors"
                            >
                                Forgot your password?
                            </a>
                        </div>

                        <!-- Submit Button -->
                        <button
                            type="submit"
                            :disabled="
                                authStore.loading ||
                                !form.email ||
                                !form.password
                            "
                            class="w-full bg-gradient-to-r from-orange-600 to-red-600 text-white py-3 px-6 rounded-xl font-bold text-lg hover:from-orange-700 hover:to-red-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-[1.02] disabled:transform-none disabled:shadow-md"
                        >
                            <span
                                v-if="authStore.loading"
                                class="flex items-center justify-center gap-2"
                            >
                                <div
                                    class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"
                                ></div>
                                Signing In...
                            </span>
                            <span
                                v-else
                                class="flex items-center justify-center gap-2"
                            >
                                <svg
                                    class="w-5 h-5"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                        stroke-width="2"
                                        d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"
                                    ></path>
                                </svg>
                                Sign In
                            </span>
                        </button>
                    </form>
                </div>

                <!-- Footer -->
                <div class="bg-gray-50 px-8 py-6 border-t border-gray-100">
                    <p class="text-center text-sm text-gray-600">
                        Don't have an account?
                        <router-link
                            to="/register"
                            class="font-medium text-orange-600 hover:text-orange-700 transition-colors ml-1"
                        >
                            Create account
                        </router-link>
                    </p>
                </div>
            </div>

            <!-- Additional Links -->
            <div class="text-center mt-8 space-y-2">
                <p class="text-xs text-gray-500">
                    By signing in, you agree to our
                    <a href="#" class="text-orange-600 hover:text-orange-700"
                        >Terms of Service</a
                    >
                    and
                    <a href="#" class="text-orange-600 hover:text-orange-700"
                        >Privacy Policy</a
                    >
                </p>
                <div class="flex items-center justify-center gap-4 pt-4">
                    <a
                        href="#"
                        class="text-gray-400 hover:text-orange-600 transition-colors"
                    >
                        <svg
                            class="w-5 h-5"
                            fill="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"
                            />
                        </svg>
                    </a>
                    <a
                        href="#"
                        class="text-gray-400 hover:text-orange-600 transition-colors"
                    >
                        <svg
                            class="w-5 h-5"
                            fill="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56.84-.6 1.56-1.36 2.14-2.23z"
                            />
                        </svg>
                    </a>
                    <a
                        href="#"
                        class="text-gray-400 hover:text-orange-600 transition-colors"
                    >
                        <svg
                            class="w-5 h-5"
                            fill="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.174-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.099.12.112.225.085.345-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.402.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.357-.629-2.746-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24.009 12.017 24.009c6.624 0 11.99-5.367 11.99-11.988C24.007 5.367 18.641.001 12.017.001z"
                            />
                        </svg>
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>
