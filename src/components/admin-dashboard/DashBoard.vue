<script setup>
    import { ref } from "vue";
    import HomeHero from "./HomeHero.vue";
</script>
<template>
    <div class="md:flex md:justify-between md:items-center">
        <div
            class="sticky top-0 md:hidden p-3 flex items-center justify-between bg-white shadow-md z-40"
        >
            <div class="flex items-center gap-4">
                <p class="md:hidden text-green-600">
                    <i class="fa-solid fa-align-left"></i>
                </p>
                <h1 class="font-styleScript text-2xl text-orange-600">
                    Vanella Pharmacy
                </h1>
            </div>
            <button class="text-gray-700">
                <router-link to="">
                    <i class="fa-solid fa-sign-out"></i>
                </router-link>
            </button>
        </div>
        <nav
            class="w-4/5 z-50 -mt-14 h-screen p-2 bg-white sticky top-0 md:mt-0 md:block md:w-1/4 lg:max-2xl:w-1/5 border-r-2 border-gray-200 md:static"
        >
            <div class="flex justify-end gap-10 items-center pt-2 md:block">
                <h1
                    class="font-styleScript text-2xl md:pt-4 md:pl-5 text-orange-600 md:text-3xl"
                >
                    Dashboard
                </h1>
                <p class="pr-2 md:hidden">
                    <i class="fa-solid fa-align-right"></i>
                </p>
            </div>
            <button class="a-dashboard-navs">
                <p><i class="fa-solid fa-house"></i></p>
                Home
            </button>
            <button class="a-dashboard-navs">
                <p><i class="fa-solid fa-user-doctor"></i></p>
                Medications
            </button>
            <button class="a-dashboard-navs">
                <p><i class="fa-solid fa-bell"></i></p>
                Orders
            </button>
            <button class="a-dashboard-navs">
                <p><i class="fa-solid fa-file"></i></p>
                Sales
            </button>
            <button class="a-dashboard-navs">
                <p>
                    <i class="fa-solid fa-universal-access"></i>
                </p>
                Notifications
            </button>
            <button
                class="mt-16 py-2 w-full pl-3 rounded text-sm font-[500] flex gap-3 text-gray-800 md:text-lg md:pl-5 md:mt-20 hover:bg-gray-100 focus:bg-orange-600 focus:text-white"
            >
                <router-link to="">
                    <i class="fa-solid fa-sign-out"></i>
                </router-link>
                Logout
            </button>
            <h1
                class="font-styleScript absolute bottom-2 right-4 text-2xl text-orange-600 md:text-[28px] md:left-3"
            >
                Vanella Pharmacy
            </h1>
        </nav>
        <div>
            <HomeHero />
        </div>
    </div>
</template>
