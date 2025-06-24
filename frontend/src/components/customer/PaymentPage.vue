<script setup>
    import { ref, computed } from "vue";
    import { useOrderStore } from "@/stores/orderStore";
    import { useRouter } from "vue-router";
    import axiosInstance from "@/services/api";
    import { useToast } from "vue-toastification";

    const orderStore = useOrderStore();
    const router = useRouter();
    const toast = useToast();

    const form = ref({
        phone: "",
        network: "",
        paymentType: "",
        amount: orderStore.pendingAmount || "",
    });

    const networkOptions = [
        { value: "mtn", label: "MTN" },
        { value: "vodafone", label: "Vodafone" },
        { value: "airteltigo", label: "AirtelTigo" },
    ];

    const paymentTypes = [{ value: "mobile_money", label: "Mobile Money" }];

    const isSubmitting = ref(false);

    const isFormValid = computed(() => {
        return (
            form.value.phone &&
            form.value.network &&
            form.value.paymentType &&
            form.value.amount
        );
    });

    const formatPhone = (value) => {
        const digits = value.replace(/\D/g, "");
        if (digits.length <= 3) return digits;
        if (digits.length <= 6)
            return `${digits.slice(0, 3)} ${digits.slice(3)}`;
        return `${digits.slice(0, 3)} ${digits.slice(3, 6)} ${digits.slice(
            6,
            10
        )}`;
    };

    const handlePhoneInput = (event) => {
        const formatted = formatPhone(event.target.value);
        form.value.phone = formatted;
    };

    const submitPayment = async () => {
        if (!isFormValid.value) return;
        isSubmitting.value = true;
        try {
            const Payload = {
                cart: orderStore.pendingOrder?.cart,
                shipping_address: orderStore.pendingOrder?.shipping_address,
                payment_details: {
                    payment_method: form.value.paymentType,
                    amount: form.value.amount,
                    currency: "GHS",
                    phone_number: form.value.phone.replace(/\s/g, ""),
                    provider: form.value.network,
                },
            };

            const orderRes = await axiosInstance.post(
                "/api/orders/create/",
                Payload
            );
            const url = orderRes.data.authorization_url;

            if (url && typeof url === "string" && url.startsWith("http")) {
                orderStore.clearPendingOrder();
                window.location.href = url;
            } else {
                toast.error("Payment URL not provided or invalid.");
                isSubmitting.value = false;
            }
        } catch (err) {
            toast.error(
                err.response?.data?.detail || "Payment initiation failed."
            );
            isSubmitting.value = false;
        }
    };
</script>

<template>
    <div
        class="min-h-screen flex items-center justify-center p-4 sm:p-6 lg:p-8 bg-gray-100 text-gray-700 font-medium"
    >
        <div
            class="w-full max-w-lg bg-white rounded-3xl shadow overflow-hidden relative border border-gray-300"
        >
            <div
                class="absolute -top-10 -right-10 w-32 h-32 bg-gray-200 rounded-full opacity-20 blur-2xl z-0"
            ></div>

            <div
                class="bg-gradient-to-r from-orange-500 to-orange-700 px-6 py-4 text-center relative z-10"
            >
                <div
                    class="w-14 h-14 bg-white/30 rounded-full flex items-center justify-center mx-auto mb-3 shadow-lg"
                >
                    <svg
                        class="w-7 h-7 text-white"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"
                        />
                    </svg>
                </div>
                <h1 class="font-medium text-white mb-1">Secure Payment</h1>
                <p class="text-white/70 text-xs">
                    Fast, safe, and reliable transactions
                </p>
            </div>

            <form
                @submit.prevent="submitPayment"
                class="p-6 space-y-4 relative z-10"
            >
                <!-- Amount -->
                <div class="space-y-2">
                    <label class="block text-sm text-gray-700"
                        >Amount (GHS)</label
                    >
                    <div class="relative">
                        <span
                            class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500"
                            >₵</span
                        >
                        <input
                            v-model="form.amount"
                            type="number"
                            step="0.01"
                            min="1"
                            required
                            placeholder="0.00"
                            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-xl focus:border-orange-500 focus:outline-none focus:ring-0 transition-all text-lg bg-white hover:bg-gray-50 focus:bg-white shadow-sm placeholder:text-sm text-gray-700"
                            :readonly="true"
                        />
                    </div>
                </div>

                <!-- Phone -->
                <div class="space-y-2">
                    <label class="block text-sm text-gray-700">Phone</label>
                    <input
                        :value="form.phone"
                        @input="handlePhoneInput"
                        type="tel"
                        required
                        placeholder="024 123 "
                        maxlength="12"
                        class="w-full pl-4 pr-4 py-2 border border-gray-300 rounded-xl focus:border-orange-500 focus:outline-none focus:ring-0 transition-all text-lg bg-white hover:bg-gray-50 focus:bg-white shadow-sm placeholder:text-sm text-gray-700"
                    />
                </div>

                <!-- Network -->
                <div class="space-y-2">
                    <label class="block text-sm text-gray-700">Network</label>
                    <div class="relative">
                        <select
                            v-model="form.network"
                            required
                            class="w-full pl-4 pr-4 py-3 border border-gray-300 rounded-xl focus:border-orange-500 focus:outline-none focus:ring-0 transition-all text-sm text-gray-700 bg-white hover:bg-gray-50 focus:bg-white appearance-none cursor-pointer shadow-sm"
                        >
                            <option value="" disabled class="text-gray-400">
                                Select network
                            </option>
                            <option
                                v-for="option in networkOptions"
                                :key="option.value"
                                :value="option.value"
                                class="text-gray-700"
                            >
                                {{ option.label }}
                            </option>
                        </select>
                        <div
                            class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none"
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
                                    d="M19 9l-7 7-7-7"
                                />
                            </svg>
                        </div>
                    </div>
                </div>

                <!-- Payment -->
                <div class="space-y-2">
                    <label class="block text-sm text-gray-700">Payment</label>
                    <div class="relative">
                        <select
                            v-model="form.paymentType"
                            required
                            class="w-full pl-4 pr-4 py-3 border border-gray-300 rounded-xl focus:border-orange-500 focus:outline-none focus:ring-0 transition-all text-sm text-gray-700 bg-white hover:bg-gray-50 focus:bg-white appearance-none cursor-pointer shadow-sm"
                        >
                            <option value="" disabled class="text-gray-400">
                                Choose method
                            </option>
                            <option
                                v-for="type in paymentTypes"
                                :key="type.value"
                                :value="type.value"
                                class="text-gray-700"
                            >
                                {{ type.label }}
                            </option>
                        </select>
                        <div
                            class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none"
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
                                    d="M19 9l-7 7-7-7"
                                />
                            </svg>
                        </div>
                    </div>
                </div>

                <!-- Submit -->
                <button
                    :disabled="!isFormValid || isSubmitting"
                    type="submit"
                    class="w-full py-3 px-6 bg-gradient-to-r from-orange-500 to-orange-700 disabled:from-gray-400 disabled:to-gray-500 text-white text-sm rounded-full shadow-xl hover:shadow-2xl disabled:shadow-none transition-all duration-200 disabled:cursor-not-allowed flex items-center justify-center gap-3 group"
                >
                    <div v-if="isSubmitting" class="flex items-center gap-2">
                        <svg
                            class="animate-spin w-5 h-5"
                            fill="none"
                            viewBox="0 0 24 24"
                        >
                            <circle
                                class="opacity-25"
                                cx="12"
                                cy="12"
                                r="10"
                                stroke="currentColor"
                                stroke-width="4"
                            />
                            <path
                                class="opacity-75"
                                fill="currentColor"
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                            />
                        </svg>
                        Processing...
                    </div>
                    <div v-else class="flex items-center gap-2">
                        Pay Now
                        <svg
                            class="w-5 h-5 group-hover:translate-x-1 transition-transform"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M13 7l5 5m0 0l-5 5m5-5H6"
                            />
                        </svg>
                    </div>
                </button>
            </form>
        </div>
    </div>
</template>
