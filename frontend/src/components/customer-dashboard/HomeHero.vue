<script setup lang="ts">
    import router from "@/router";
</script>

<template>
    <div class="h-screen w-full relative flex flex-col flex-1 overflow-hidden">
        <div
            class="hidden md:block w-full md:absolute top-0 z-50 p-3 bg-gray-900"
        >
            <h1
                class="text-gray-300 font-styleScript text-center text-lg md:text-2xl"
            >
                Welcome, Jane Doe
            </h1>
        </div>
        <div class="mx-auto container m-4 md:mt-[75px]">
            <div
                class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 p-3"
            >
                <div
                    class="flex items-center justify-between rounded-lg shadow hover:shadow-md transition-shadow p-6 bg-white"
                >
                    <div>
                        <p class="text-gray-500 font-medium text-sm">
                            Total Orders
                        </p>
                        <p
                            class="text-2xl font-semibold font-poppins text-green-500"
                        >
                            5
                        </p>
                    </div>
                    <i
                        class="pi pi-cart-arrow-down text-green-500 text-2xl"
                    ></i>
                </div>

                <div
                    class="flex items-center justify-between rounded-lg shadow hover:shadow-md transition-shadow p-6 bg-white"
                >
                    <div>
                        <p class="text-gray-500 font-medium text-sm">
                            Notifications
                        </p>
                        <p
                            class="text-2xl font-semibold font-poppins text-red-500"
                        >
                            10
                        </p>
                    </div>
                    <i class="pi pi-info-circle text-red-500 text-2xl"></i>
                </div>

                <div
                    class="flex items-center justify-between rounded-lg shadow hover:shadow-md transition-shadow p-6 bg-white"
                >
                    <div>
                        <p class="text-gray-500 font-medium text-sm">
                            Pending Deliveries
                        </p>
                        <p
                            class="text-2xl font-semibold font-poppins text-blue-500"
                        >
                            50
                        </p>
                    </div>
                    <i
                        class="pi pi-spinner-dotted animate-spin text-blue-500 text-2xl"
                    ></i>
                </div>

                <div
                    class="flex items-center justify-between rounded-lg shadow hover:shadow-md transition-shadow p-6 bg-white"
                >
                    <div>
                        <p class="text-gray-500 font-medium text-sm">
                            cart Level
                        </p>
                        <p
                            class="text-2xl font-semibold font-poppins text-yellow-500"
                        >
                            70%
                        </p>
                    </div>
                    <i class="pi pi-chart-bar text-yellow-500 text-2xl"></i>
                </div>
            </div>
        </div>
    </div>
</template>
