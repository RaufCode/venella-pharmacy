<script setup lang="ts">
    import router from "@/router";
</script>

<template>
    <div class="h-screen overflow-y-auto w-full">
        <div class="max-w-[1440px] mx-auto">
            <div
                class="w-full sticky top-0 z-40 bg-gray-50 shadow-md flex justify-between items-center p-3"
            >
                <h1 class="text-gray-600 text-lg font-semibold md:text-2xl">
                    Welcome Mr.You
                </h1>
            </div>
            <div
                class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 p-3 h-screen"
            >
                <router-link to="">
                    <div
                        class="flex items-center justify-between rounded-lg shadow hover:shadow-md transition-shadow p-6 bg-white"
                    >
                        <div>
                            <p class="text-gray-500 font-medium text-sm">
                                Total Sales
                            </p>
                            <p
                                class="text-2xl font-semibold font-poppins text-green-500"
                            >
                                &#8373;15
                            </p>
                        </div>
                        <i class="pi pi-book text-green-500 text-2xl"></i>
                    </div>
                </router-link>
                <router-link to="">
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
                </router-link>
                <router-link to="">
                    <div
                        class="flex items-center justify-between rounded-lg shadow hover:shadow-md transition-shadow p-6 bg-white"
                    >
                        <div>
                            <p class="text-gray-500 font-medium text-sm">
                                Pending Ords
                            </p>
                            <p
                                class="text-2xl font-semibold font-poppins text-blue-500"
                            >
                                50
                            </p>
                        </div>
                        <i
                            class="pi pi-star-half-fill text-blue-500 text-2xl"
                        ></i>
                    </div>
                </router-link>
                <router-link to="">
                    <div
                        class="flex items-center justify-between rounded-lg shadow hover:shadow-md transition-shadow p-6 bg-white"
                    >
                        <div>
                            <p class="text-gray-500 font-medium text-sm">
                                Stock Level
                            </p>
                            <p
                                class="text-2xl font-semibold font-poppins text-yellow-500"
                            >
                                70%
                            </p>
                        </div>
                        <i class="pi pi-chart-bar text-yellow-500 text-2xl"></i>
                    </div>
                </router-link>
            </div>
        </div>
    </div>
</template>
