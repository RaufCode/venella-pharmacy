<script setup>
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
    <div
        class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-orange-50 flex items-center justify-center p-4"
    >
        <div class="w-full max-w-2xl">
            <!-- Logo and Header -->
            <div class="text-center mb-8">
                <div
                    class="w-16 h-16 bg-gradient-to-br from-orange-500 to-red-600 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg"
                >
                    <span class="text-white font-bold text-2xl">V</span>
                </div>
                <h1
                    class="text-3xl font-styleScript bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent mb-2"
                >
                    Join VPharm
                </h1>
                <p class="text-gray-600">
                    Create account to start your healthcare journey
                </p>
            </div>

            <!-- Sign Up Form -->
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

                    <form @submit.prevent="validation" class="space-y-6">
                        <!-- Name Fields -->
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label
                                    class="block text-sm font-medium text-gray-700 mb-2"
                                >
                                    First Name *
                                </label>
                                <div class="relative">
                                    <input
                                        v-model="form.first_name"
                                        type="text"
                                        name="first_name"
                                        required
                                        :disabled="authStore.loading"
                                        class="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-all duration-200 disabled:bg-gray-100 disabled:cursor-not-allowed pl-12"
                                        placeholder="Enter first name"
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
                                                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                                            ></path>
                                        </svg>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <label
                                    class="block text-sm font-medium text-gray-700 mb-2"
                                >
                                    Last Name *
                                </label>
                                <div class="relative">
                                    <input
                                        v-model="form.last_name"
                                        type="text"
                                        name="last_name"
                                        required
                                        :disabled="authStore.loading"
                                        class="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-all duration-200 disabled:bg-gray-100 disabled:cursor-not-allowed pl-12"
                                        placeholder="Enter last name"
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
                                                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                                            ></path>
                                        </svg>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Other Names and Email -->
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label
                                    class="block text-sm font-medium text-gray-700 mb-2"
                                >
                                    Other Names
                                </label>
                                <div class="relative">
                                    <input
                                        v-model="form.other_names"
                                        type="text"
                                        name="other_names"
                                        :disabled="authStore.loading"
                                        class="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-all duration-200 disabled:bg-gray-100 disabled:cursor-not-allowed pl-12"
                                        placeholder="Middle name (optional)"
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
                                                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                                            ></path>
                                        </svg>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <label
                                    class="block text-sm font-medium text-gray-700 mb-2"
                                >
                                    Email Address *
                                </label>
                                <div class="relative">
                                    <input
                                        v-model="form.email"
                                        type="email"
                                        name="email"
                                        autocomplete="email"
                                        required
                                        :disabled="authStore.loading"
                                        class="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-all duration-200 disabled:bg-gray-100 disabled:cursor-not-allowed pl-12"
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
                        </div>

                        <!-- Phone and Address -->
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label
                                    class="block text-sm font-medium text-gray-700 mb-2"
                                >
                                    Phone Number *
                                </label>
                                <div class="relative">
                                    <input
                                        v-model="form.phone"
                                        type="tel"
                                        name="phone"
                                        required
                                        :disabled="authStore.loading"
                                        class="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-all duration-200 disabled:bg-gray-100 disabled:cursor-not-allowed pl-12"
                                        placeholder="0XX XXX XXXX"
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
                                                d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
                                            ></path>
                                        </svg>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <label
                                    class="block text-sm font-medium text-gray-700 mb-2"
                                >
                                    Address *
                                </label>
                                <div class="relative">
                                    <input
                                        v-model="form.address"
                                        type="text"
                                        name="address"
                                        required
                                        :disabled="authStore.loading"
                                        class="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-all duration-200 disabled:bg-gray-100 disabled:cursor-not-allowed pl-12"
                                        placeholder="Enter your address"
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
                                                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                                            ></path>
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                stroke-width="2"
                                                d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                                            ></path>
                                        </svg>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Password -->
                        <div>
                            <label
                                class="block text-sm font-medium text-gray-700 mb-2"
                            >
                                Password *
                            </label>
                            <div class="relative">
                                <input
                                    v-model="form.password"
                                    type="password"
                                    name="password"
                                    autocomplete="new-password"
                                    required
                                    :disabled="authStore.loading"
                                    class="w-full border border-gray-300 rounded-xl px-4 py-3 text-gray-800 placeholder-gray-500 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-all duration-200 disabled:bg-gray-100 disabled:cursor-not-allowed pl-12"
                                    placeholder="Create password"
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
                            <p class="text-xs text-gray-500 mt-2">
                                Password should be at least 8 characters
                            </p>
                        </div>

                        <!-- Terms and Conditions -->
                        <div class="flex items-start gap-3">
                            <input
                                type="checkbox"
                                id="terms"
                                required
                                :disabled="authStore.loading"
                                class="mt-1 w-4 h-4 text-orange-600 border-gray-300 rounded focus:ring-orange-500 focus:ring-2"
                            />
                            <label for="terms" class="text-sm text-gray-600">
                                I agree to the
                                <a
                                    href="#"
                                    class="text-orange-600 hover:text-orange-700 font-medium"
                                    >Terms of Service</a
                                >
                                and
                                <a
                                    href="#"
                                    class="text-orange-600 hover:text-orange-700 font-medium"
                                    >Privacy Policy</a
                                >
                            </label>
                        </div>

                        <!-- Submit Button -->
                        <button
                            type="submit"
                            :disabled="
                                authStore.loading ||
                                !form.first_name ||
                                !form.last_name ||
                                !form.email ||
                                !form.phone ||
                                !form.address ||
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
                                Creating...
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
                                        d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
                                    ></path>
                                </svg>
                                Create
                            </span>
                        </button>
                    </form>
                </div>

                <!-- Footer -->
                <div class="bg-gray-50 px-8 py-6 border-t border-gray-100">
                    <p class="text-center text-sm text-gray-600">
                        Already have an account?
                        <router-link
                            to="/login"
                            class="font-medium text-orange-600 hover:text-orange-700 transition-colors ml-1"
                        >
                            Sign in here
                        </router-link>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>
