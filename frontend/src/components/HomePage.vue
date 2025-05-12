<script setup>
    import Btn from "../components/ui/Btn.vue";
</script>

<template>
    <div class="m-0 p-0">
        <div class="shadow-md fixed top-0 w-full bg-white z-10">
            <div
                class="flex justify-between items-center text-sm p-4 md:text-lg md:px-6 lg:px-10 max-w-[1440px] mx-auto"
            >
                <router-link to="" class="text-blue-600 block font-semibold">
                    <i class="pi pi-slack text-2xl"></i>
                </router-link>
                <h1 class="hidden md:flex text-blue-600 font-medium">
                    <marquee>Venella Pharmacy</marquee>
                    <!--I know marquee is deprecated though-->
                </h1>
                <div class="flex gap-2 items-center md:gap-4">
                    <router-link
                        to="/register"
                        class="bg-orange-600 block font-medium py-1 px-3 text-white text-base hover:bg-orange-500"
                    >
                        Sign up
                    </router-link>
                    <router-link
                        to="/login"
                        class="bg-orange-600 block font-medium py-1 px-3 text-white text-base hover:bg-orange-500"
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
        <div class="bg-white">
            <h1
                class="py-3 text-lg font-medium text-orange-600 text-center md:font-semibold"
            >
                Top Picks for You
            </h1>
            <div
                class="px-4 mb-5 mx-auto grid grid-cols-2 gap-3 lg:grid-cols-4 md:px-6 md:gap-5 md:mb-8 max-w-[1440px]"
            >
                <div
                    class="bg-[url('/drug1.jpg')] bg-no-repeat bg-cover p-1 rounded-xl transition-transform duration-300 hover:shadow-md shadow-black"
                >
                    <div
                        class="bg-black bg-opacity-60 rounded-b-xl mt-40 md:mt-48"
                    >
                        <h1 class="text-center text-white p-1">
                            <router-link to="/login" class="block">
                                Pain Relief
                            </router-link>
                        </h1>
                    </div>
                </div>
                <div
                    class="bg-gray-500 bg-[url('/drug2.jpg')] bg-no-repeat bg-cover p-1 rounded-xl transition-transform duration-300 hover:shadow-md shadow-black"
                >
                    <div
                        class="bg-black bg-opacity-60 rounded-b-xl mt-40 md:mt-48"
                    >
                        <h1 class="text-center text-white p-1">
                            <router-link to="/login" class="block">
                                Cold & Flu
                            </router-link>
                        </h1>
                    </div>
                </div>
                <div
                    class="bg-gray-500 bg-[url('/drug3.jpg')] bg-no-repeat bg-cover p-1 rounded-xl transition-transform duration-300 hover:shadow-md shadow-black"
                >
                    <div
                        class="bg-black bg-opacity-60 rounded-b-xl mt-40 md:mt-48"
                    >
                        <h1 class="text-center text-white p-1">
                            <router-link to="/login" class="block">
                                Supplements
                            </router-link>
                        </h1>
                    </div>
                </div>
                <div
                    class="bg-gray-500 bg-[url('/drug4.jpg')] bg-no-repeat bg-cover p-1 rounded-xl transition-transform duration-300 hover:shadow-md shadow-black"
                >
                    <div
                        class="bg-black bg-opacity-60 rounded-b-xl mt-40 md:mt-48"
                    >
                        <h1 class="text-center text-white p-1">
                            <router-link to="/login" class="block">
                                Antibiotics
                            </router-link>
                        </h1>
                    </div>
                </div>

                <div
                    class="bg-gray-500 bg-[url('/syrup1.jpg')] bg-no-repeat bg-cover p-1 rounded-xl transition-transform duration-300 hover:shadow-md shadow-black"
                >
                    <div
                        class="bg-black bg-opacity-60 rounded-b-xl mt-40 md:mt-48"
                    >
                        <h1 class="text-center text-white p-1">
                            <router-link to="/login" class="block">
                                Gut Flow
                            </router-link>
                        </h1>
                    </div>
                </div>
                <div
                    class="bg-gray-500 bg-[url('/vitamin.jpg')] bg-no-repeat bg-cover p-1 rounded-xl transition-transform duration-300 hover:shadow-md shadow-black"
                >
                    <div
                        class="bg-black bg-opacity-60 rounded-b-xl mt-40 md:mt-48"
                    >
                        <h1 class="text-center text-white p-1">
                            <router-link to="/login" class="block">
                                Vitamins
                            </router-link>
                        </h1>
                    </div>
                </div>
                <div
                    class="bg-gray-500 bg-[url('/drug5.jpg')] bg-no-repeat bg-cover p-1 rounded-xl transition-transform duration-300 hover:shadow-md shadow-black"
                >
                    <div
                        class="bg-black bg-opacity-60 rounded-b-xl mt-40 md:mt-48"
                    >
                        <h1 class="text-center text-white p-1">
                            <router-link to="/login" class="block">
                                Syrup
                            </router-link>
                        </h1>
                    </div>
                </div>
                <div
                    class="bg-gray-500 bg-[url('/skincare.jpg')] bg-no-repeat bg-cover p-1 rounded-xl transition-transform duration-300 hover:shadow-md shadow-black"
                >
                    <div
                        class="bg-black bg-opacity-60 rounded-b-xl mt-40 md:mt-48"
                    >
                        <h1 class="text-center text-white p-1">
                            <router-link to="/login" class="block">
                                Skin Care
                            </router-link>
                        </h1>
                    </div>
                </div>
            </div>
        </div>
        <!--DeliverySection-->
        <div class="bg-gray-50 py-3 px-4 text-center md:py-5 md:px-6">
            <h2 class="text-lg font-semibold text-orange-600 my-2">
                Fast & Reliable Delivery
            </h2>
            <p class="text-gray-600 mb-3">
                Get your medicines delivered to your doorstep in no time
            </p>
            <img
                src="../../delivery.png"
                alt="a picture of a delivery man"
                class="rounded-md w-full md:w-[500px] mx-auto"
            />
            <button
                class="px-4 py-2 bg-orange-600 text-white text-base font-medium hover:bg-orange-700 transition"
            >
                Order Now
            </button>
        </div>
        <!--FooterSection-->
        <div class="bg-gray-800 px-4 py-5 grid place-items-center">
            <div
                class="grid grid-cols-1 gap-9 lg:w-full lg:grid-cols-3 md:px-6 max-w-[1440px]"
            >
                <div class="">
                    <h2
                        class="text-sm font-semibold text-blue-500 py-3 md:py-5"
                    >
                        Let's Connect
                    </h2>
                    <p
                        class="text-gray-400 text-sm flex items-center gap-3 pb-4"
                    >
                        <i class="pi pi-ethereum block text-white"></i>
                        Market junction, Kumasi, Ghana
                    </p>
                    <p
                        class="text-gray-400 text-sm flex items-center gap-3 pb-4"
                    >
                        <i class="pi pi-phone block text-white"></i> +233 XXX
                        XXX XXX
                    </p>
                    <p
                        class="text-gray-400 text-sm flex items-center gap-3 pb-4"
                    >
                        <i class="pi pi-whatsapp block text-white"></i> +233 XXX
                        XXX XXX
                    </p>
                    <p class="text-gray-400 text-sm flex items-center gap-3">
                        <i class="pi pi-envelope block text-white"></i>
                        support@vanellepharmacy.com
                    </p>
                </div>
                <div>
                    <h2
                        class="font-semibold text-sm text-blue-500 py-3 md:py-5"
                    >
                        Join us on
                    </h2>
                    <div class="flex gap-4 w-max">
                        <a href="" class="text-gray-400 hover:text-white">
                            <i class="pi pi-facebook text-xl"></i>
                        </a>
                        <a href="#" class="text-gray-400 hover:text-white">
                            <i class="pi pi-instagram text-xl"></i>
                        </a>
                        <a href="#" class="text-gray-400 hover:text-white">
                            <i class="pi pi-twitter text-xl"></i>
                        </a>
                        <a href="#" class="text-gray-400 hover:text-white">
                            <i class="pi pi-tiktok text-xl"></i>
                        </a>
                        <a href="#" class="text-gray-400 hover:text-white">
                            <i class="pi pi-linkedin text-xl"></i>
                        </a>
                        <a href="#" class="text-gray-400 hover:text-white">
                            <i class="pi pi-google text-xl"></i>
                        </a>
                    </div>
                </div>
                <div class="">
                    <h2
                        class="text-sm font-semibold text-blue-500 py-3 md:py-5"
                    >
                        Contact Us
                    </h2>
                    <form
                        class="md:w-[300px] lg:w-auto max-w-[450px] space-y-3 text-center text-sm text-white"
                    >
                        <input
                            type="text"
                            required
                            placeholder="Your Name"
                            class="block mt-1 w-full mx-auto border border-gray-400 rounded outline-none focus:border-orange-700 h-9 px-4 md:h-10 bg-transparent"
                        />
                        <input
                            type="email"
                            required
                            placeholder="Your Email"
                            class="block mt-1 w-full mx-auto border border-gray-400 rounded outline-none focus:border-orange-700 h-9 px-4 md:h-10 bg-transparent"
                        />
                        <textarea
                            rows="3"
                            required
                            placeholder="Your Message"
                            class="w-full p-4 rounded-md bg-transparent border border-gray-400 text-white placeholder-gray-400 outline-none focus:border-orange-700 resize-none"
                        ></textarea>
                        <Btn btnName="Send Messsage" />
                    </form>
                </div>
            </div>
        </div>
        <!--CopyRightSection-->

        <div class="py-4 text-center text-gray-400 text-sm bg-gray-800">
            <p>&copy; Vanelle Pharmacy - All Rights Reserved</p>
        </div>
        <div class="bg-gray-800 px-4 md:px-6 lg:px-10 pt-5">
            <div
                class="max-w-[1440px] border-t border-gray-400 pt-5 md:mx-auto md:w-[300px] lg:w-auto"
            >
                <p class="text-white text-lg font-semibold flex gap-3 pb-4">
                    <i class="pi pi-slack text-blue-600 text-2xl"></i>venella
                    pharmacy
                </p>
            </div>
        </div>
    </div>
</template>
