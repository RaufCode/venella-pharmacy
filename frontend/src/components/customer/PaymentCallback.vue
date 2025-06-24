<script setup>
    import { onMounted, ref } from "vue";
    import { useRouter, useRoute } from "vue-router";
    import axiosInstance from "@/services/api";

    const router = useRouter();
    const route = useRoute();

    const isLoading = ref(true);
    const status = ref("");
    const errorMsg = ref("");

    onMounted(async () => {
        const reference = route.query.reference;

        if (!reference) {
            isLoading.value = false;
            status.value = "error";
            errorMsg.value = "No payment reference found.";
            return;
        }

        try {
            const res = await axiosInstance.post(
                `/api/payments/verify/${reference}/`
            );
            if (res.data.payment.status === "completed") {
                status.value = "completed";
            } else {
                status.value = "error";
                errorMsg.value =
                    res.data.message || "Payment verification failed.";
            }
        } catch (error) {
            status.value = "error";
            errorMsg.value =
                error.response?.data?.detail || "Could not verify payment.";
        } finally {
            isLoading.value = false;
        }
    });
</script>

<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
        <div
            class="bg-white max-w-md w-full p-8 rounded-2xl shadow-xl text-center"
        >
            <!-- Verifying State -->
            <div v-if="isLoading" class="space-y-3">
                <div
                    class="mx-auto w-10 h-10 border-4 border-orange-500 border-t-transparent rounded-full animate-spin"
                />
                <p class="text-lg font-medium text-gray-700">
                    Verifying payment...
                </p>
            </div>

            <!-- Payment Success -->
            <div v-else-if="status === 'completed'" class="space-y-4">
                <div class="text-green-600">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-16 w-16 mx-auto"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M5 13l4 4L19 7"
                        />
                    </svg>
                </div>
                <p class="text-xl font-bold text-green-600">
                    Payment Successful!
                </p>
                <p class="text-gray-600">
                    Your order has been placed successfully.
                </p>
                <button
                    @click="() => router.replace('/orders')"
                    class="mt-4 block mx-auto px-6 py-2 bg-orange-500 text-white rounded-full font-medium hover:bg-orange-600 transition"
                >
                    View Orders
                </button>
            </div>
            <!-- Payment Error -->
            <div v-else class="space-y-4">
                <div class="text-red-600">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-16 w-16 mx-auto"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M6 18L18 6M6 6l12 12"
                        />
                    </svg>
                </div>
                <p class="text-xl font-bold text-red-600">Payment Failed</p>
                <p class="text-gray-600">{{ errorMsg }}</p>
                <button
                    @click="() => router.replace('/')"
                    class="mt-4 block mx-auto px-6 py-2 bg-orange-500 text-white rounded-full font-medium hover:bg-orange-600 transition"
                >
                    Go Home
                </button>
            </div>
        </div>
    </div>
</template>
