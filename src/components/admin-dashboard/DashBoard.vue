<script setup>
    import { ref } from "vue";
    // import OverView from "./OverView.vue";
    import MedicationHero from "./MedicationHero.vue";
</script>
<template>
    <div class="md:flex md:justify-start md:items-center">
        <div
            class="sticky top-0 md:hidden p-3 text-sm flex items-center justify-between bg-white shadow-md z-40"
        >
            <div class="flex items-center gap-4">
                <p>
                    <i class="pi pi-align-left"></i>
                </p>
                <h1 class="font-styleScript text-2xl text-orange-600">
                    Vanella Pharmacy
                </h1>
            </div>
            <button class="text-gray-700">
                <router-link to="">
                    <i class="pi pi-sign-out"></i>
                </router-link>
            </button>
        </div>
        <aside
            class="hidden w-4/5 z-50 -mt-14 h-screen p-2 bg-gray-50 sticky top-0 md:mt-0 md:block md:max-w-[210px] lg:max-w-[220px] border-r-2 border-gray-200"
        >
            <div class="flex justify-end gap-10 items-center pt-2 md:block">
                <h1
                    class="font-styleScript text-2xl md:pt-4 md:pb-3 md:pl-5 text-orange-600 md:text-3xl"
                >
                    Dashboard
                </h1>
                <p class="pr-2 md:hidden">
                    <i class="pi pi-align-right"></i>
                </p>
            </div>
            <button class="a-dashboard-navs">
                <p>
                    <i class="pi pi-home"></i>
                </p>
                Overview
            </button>
            <button class="a-dashboard-navs">
                <p><i class="pi pi-shield"></i></p>
                Medications
            </button>
            <button class="a-dashboard-navs">
                <p><i class="pi pi-shopping-cart"></i></p>
                Orders
            </button>
            <button class="a-dashboard-navs">
                <p><i class="pi pi-book"></i></p>
                Sales
            </button>
            <button class="a-dashboard-navs">
                <p>
                    <i class="pi pi-info-circle"></i>
                </p>
                Notifications
            </button>
            <button
                class="mt-16 py-2 w-full pl-3 rounded font-medium text-sm flex gap-4 text-gray-800 md:pl-5 md:mt-20 hover:bg-gray-100 focus:bg-orange-600 focus:text-white"
            >
                <router-link to="">
                    <i class="pi pi-sign-out"></i>
                </router-link>
                Logout
            </button>
        </aside>
        <div class="bg-gray-50 w-full">
            <div class="min-h-screen max-w-[1440px]">
                <!-- <OverView /> -->
                <MedicationHero />
            </div>
        </div>
    </div>
</template>
