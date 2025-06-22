<script setup>
    import { useRouter } from "vue-router";
    const router = useRouter();
    function goHome() {
        router.push("/");
    }
</script>

<template>
    <div
        class="min-h-screen flex flex-col items-center justify-center px-4 bg-gray-50"
    >
        <div
            class="max-w-lg w-full p-10 rounded-3xl shadow-xl border-2 border-orange-200 flex flex-col items-center bg-white"
        >
            <svg
                class="w-24 h-24 text-orange-400 mb-6"
                fill="none"
                stroke="currentColor"
                stroke-width="1.5"
                viewBox="0 0 24 24"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
            </svg>
            <h1
                class="text-4xl font-extrabold text-orange-600 mb-2 font-montserrat"
            >
                404
            </h1>
            <h2 class="text-2xl font-bold text-orange-500 mb-4">
                Page Not Found
            </h2>
            <p class="text-orange-700 text-center mb-8">
                Sorry, this page doesn't exist.
            </p>
            <button
                @click="goHome"
                class="px-6 py-3 rounded-lg bg-gradient-to-r from-orange-500 to-orange-600 text-white font-bold shadow hover:from-orange-600 hover:to-orange-700 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-400"
            >
                Home
            </button>
        </div>
    </div>
</template>
