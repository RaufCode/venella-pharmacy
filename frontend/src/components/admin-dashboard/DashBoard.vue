<script setup>
    import { ref } from "vue";
    import OverView from "./OverView.vue";
    import MedicationHero from "./MedicationHero.vue";
    import SalesHero from "./SalesHero.vue";
    import StaffHero from "./StaffHero.vue";

    const activeTab = ref("overview");
    const hamburger = ref(false);
</script>
<template>
    <div class="md:flex md:justify-start">
        <div
            class="sticky top-0 md:hidden p-3 text-sm flex items-center justify-between bg-white shadow-md z-50 w-full"
        >
            <div class="flex items-center gap-4">
                <p @click="hamburger = !hamburger">
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
            :class="{
                block: hamburger,
                hidden: !hamburger,
                'md:block md:static': true,
            }"
            class="w-4/5 z-50 bg-gray-50 fixed top-0 min-h-screen md:min-w-[210px] md:max-w-[210px] lg:min-w-[220px] lg:max-w-[220px] border-r-2 border-gray-200 text-gray-800"
        >
            <div class="flex justify-end gap-10 items-center pt-2 md:block">
                <h1
                    class="font-styleScript text-2xl md:pt-4 md:pb-3 md:pl-5 text-orange-600 md:text-3xl"
                >
                    Dashboard
                </h1>
                <p @click="hamburger = !hamburger" class="pr-2 md:hidden">
                    <i class="pi pi-align-right"></i>
                </p>
            </div>
            <button
                @click="activeTab = 'overview'"
                class="a-dashboard-navs"
                :class="{
                    'bg-orange-600 text-white hover:bg-orange-500':
                        activeTab === 'overview',
                }"
            >
                <p>
                    <i class="pi pi-home"></i>
                </p>
                Overview
            </button>
            <button
                @click="activeTab = 'medication'"
                class="a-dashboard-navs"
                :class="{
                    'bg-orange-600 text-white hover:bg-orange-500':
                        activeTab === 'medication',
                }"
            >
                <p><i class="pi pi-shield"></i></p>
                Medications
            </button>
            <button
                @click="activeTab = 'sales'"
                class="a-dashboard-navs"
                :class="{
                    'bg-orange-600 text-white hover:bg-orange-500':
                        activeTab === 'sales',
                }"
            >
                <p><i class="pi pi-book"></i></p>
                Sales
            </button>
            <button
                @click="activeTab = 'staff'"
                class="a-dashboard-navs"
                :class="{
                    'bg-orange-600 text-white hover:bg-orange-500':
                        activeTab === 'staff',
                }"
            >
                <p><i class="pi pi-shopping-cart"></i></p>
                Staff
            </button>
            <button class="a-dashboard-navs">
                <p>
                    <i class="pi pi-info-circle"></i>
                </p>
                Notifications
            </button>
            <router-link to="/login">
                <button
                    class="mt-16 py-2 w-full pl-3 rounded font-medium text-sm flex items-center gap-4 text-gray-800 md:pl-5 md:mt-20 hover:bg-gray-100 focus:bg-orange-600 focus:text-white"
                >
                    <i class="pi pi-sign-out"></i>
                    Logout
                </button>
            </router-link>
        </aside>
        <div class="bg-gray-50 w-full">
            <div class="">
                <OverView v-if="activeTab === 'overview'" />
                <MedicationHero v-if="activeTab === 'medication'" />
                <SalesHero v-if="activeTab === 'sales'" />
                <StaffHero v-if="activeTab === 'staff'" />
            </div>
        </div>
    </div>
</template>
