<script setup></script>

<template>
    <div class="">
        <div class="shadow-md fixed top-0 w-full bg-white z-10">
            <div
                class="flex justify-between items-center text-sm p-4 md:text-lg md:px-6 lg:px-10 max-w-[1440px] mx-auto"
            >
                <router-link to="" class="text-blue-600 block font-semibold">
                    <i class="pi pi-slack text-2xl"></i>
                </router-link>
                <h1 class="hidden md:flex text-blue-600 font-medium">
                    <marquee>Venella Pharmacy</marquee>
                </h1>
                <div class="flex gap-2 items-center md:gap-4">
                    <router-link
                        to="/signup"
                        class="bg-orange-600 block font-medium py-1 px-3 rounded text-white hover:bg-orange-500"
                    >
                        Sign up
                    </router-link>
                    <router-link
                        to="/signin"
                        class="bg-orange-600 block font-medium py-1 px-3 rounded text-white hover:bg-orange-500"
                    >
                        Sign in
                    </router-link>
                </div>
            </div>
        </div>
        <!--HomeSection-->
        <div class="h-svh flex justify-center items-center bg-gray-50">
            <div>
                <div class="px-4">
                    <h1
                        class="font-styleScript text-[29px] text-orange-600 md:text-4xl"
                    >
                        Welcome to Venella Pharmacy
                    </h1>
                    <p class="text-gray-800 pb-2">
                        Your trusted partner in health and wellness
                    </p>
                </div>
                <div
                    class="flex justify-start gap-2 items-center text-sm w-full max-w-[500px] relative px-4"
                >
                    <label class="w-4/5">
                        <input
                            type="search"
                            placeholder="Search for medicine"
                            class="border border-gray-400 rounded outline-none w-full focus:border-orange-700 h-10 pl-5"
                        />
                    </label>
                    <button
                        class="bg-orange-600 h-10 text-white rounded px-2 hover:bg-orange-500 shadow-md transition-all duration-500"
                    >
                        Search
                    </button>
                    <div
                        class="hidden w-full absolute top-11 bg-gray-50 shadow p-2 z-20"
                    >
                        <h1>Medication List</h1>
                    </div>
                </div>
            </div>
        </div>
        <!--MedicationSection-->
        <div>
            <section class="py-10 px-5">
                <h2 class="text-2xl font-semibold text-gray-800 text-center">
                    Featured Products
                </h2>
                <div
                    class="mt-6 grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6"
                >
                    <div class="p-4 border rounded-lg shadow-md text-center">
                        <img
                            src="https://via.placeholder.com/150"
                            alt="Medicine"
                            class="mx-auto w-24 h-24"
                        />
                        <h3 class="mt-3 font-medium text-gray-800">
                            Pain Reliever
                        </h3>
                        <p class="text-gray-600">$5.99</p>
                        <button
                            class="mt-3 px-4 py-2 bg-orange-600 text-white rounded hover:bg-orange-700 transition"
                        >
                            Order Now
                        </button>
                    </div>
                    <div class="p-4 border rounded-lg shadow-md text-center">
                        <img
                            src="https://via.placeholder.com/150"
                            alt="Medicine"
                            class="mx-auto w-24 h-24"
                        />
                        <h3 class="mt-3 font-medium text-gray-800">
                            Cough Syrup
                        </h3>
                        <p class="text-gray-600">$8.50</p>
                        <button
                            class="mt-3 px-4 py-2 bg-orange-600 text-white rounded hover:bg-orange-700 transition"
                        >
                            Order Now
                        </button>
                    </div>
                    <div class="p-4 border rounded-lg shadow-md text-center">
                        <img
                            src="https://via.placeholder.com/150"
                            alt="Medicine"
                            class="mx-auto w-24 h-24"
                        />
                        <h3 class="mt-3 font-medium text-gray-800">
                            Vitamin C Tablets
                        </h3>
                        <p class="text-gray-600">$12.00</p>
                        <button
                            class="mt-3 px-4 py-2 bg-orange-600 text-white rounded hover:bg-orange-700 transition"
                        >
                            Order Now
                        </button>
                    </div>
                    <div class="p-4 border rounded-lg shadow-md text-center">
                        <img
                            src="../../public/favicon.ico"
                            alt="Medicine"
                            class="mx-auto w-24 h-24"
                        />
                        <h3 class="mt-3 font-medium text-gray-800">
                            Antibiotics
                        </h3>
                        <p class="text-gray-600">$15.00</p>
                        <button
                            class="mt-3 px-4 py-2 bg-orange-600 text-white rounded hover:bg-orange-700 transition"
                        >
                            Order Now
                        </button>
                    </div>
                </div>
            </section>
        </div>
    </div>
</template>
