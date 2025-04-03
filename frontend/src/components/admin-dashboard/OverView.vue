<script setup lang="ts">
    import router from "@/router";
</script>

<template>
    <div class="p-3 min-h-screen overflow-y-scroll md:px-5">
        <div class="pt-10 md:pt-5">
            <h1 class="text-3xl font-styleScript text-orange-600">
                Welcome to Admin Dashboard
            </h1>
            <p class="tracking-widest text-sm mb-3">
                Manage your pharmacy operations efficiently and effectively.
            </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
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
                    <i class="pi pi-star-half-fill text-blue-500 text-2xl"></i>
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
</template>
