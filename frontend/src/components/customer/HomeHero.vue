<script setup lang="ts">
    import router from "@/router";
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-orange-50">
        <!-- Welcome Header -->
        <div class="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 text-white">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div class="text-center">
                    <div class="flex items-center justify-center gap-3 mb-2">
                        <div class="w-10 h-10 bg-gradient-to-br from-orange-500 to-red-600 rounded-xl flex items-center justify-center">
                            <span class="text-white font-bold text-lg">V</span>
                        </div>
                        <h1 class="text-2xl md:text-3xl font-bold bg-gradient-to-r from-orange-400 to-red-400 bg-clip-text text-transparent">
                            Welcome Back!
                        </h1>
                    </div>
                    <p class="text-gray-300 text-lg font-styleScript">Your health dashboard awaits</p>
                </div>
            </div>
        </div>

        <!-- Dashboard Content -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Quick Actions -->
            <div class="mb-8">
                <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
                    <svg class="w-7 h-7 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                    </svg>
                    Quick Actions
                </h2>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <button
                        @click="router.push('/')"
                        class="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-xl hover:border-orange-200 transition-all duration-200 transform hover:scale-105 group"
                    >
                        <div class="w-12 h-12 bg-gradient-to-br from-blue-100 to-blue-200 rounded-lg flex items-center justify-center mx-auto mb-3 group-hover:from-blue-200 group-hover:to-blue-300 transition-all duration-200">
                            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
                            </svg>
                        </div>
                        <p class="font-semibold text-gray-800 text-sm">Shop Products</p>
                        <p class="text-xs text-gray-600 mt-1">Browse medications</p>
                    </button>

                    <button
                        @click="router.push('/orders')"
                        class="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-xl hover:border-orange-200 transition-all duration-200 transform hover:scale-105 group"
                    >
                        <div class="w-12 h-12 bg-gradient-to-br from-green-100 to-green-200 rounded-lg flex items-center justify-center mx-auto mb-3 group-hover:from-green-200 group-hover:to-green-300 transition-all duration-200">
                            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                            </svg>
                        </div>
                        <p class="font-semibold text-gray-800 text-sm">My Orders</p>
                        <p class="text-xs text-gray-600 mt-1">Track deliveries</p>
                    </button>

                    <button
                        @click="router.push('/cart')"
                        class="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-xl hover:border-orange-200 transition-all duration-200 transform hover:scale-105 group"
                    >
                        <div class="w-12 h-12 bg-gradient-to-br from-orange-100 to-orange-200 rounded-lg flex items-center justify-center mx-auto mb-3 group-hover:from-orange-200 group-hover:to-orange-300 transition-all duration-200">
                            <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.293 2.293A1 1 0 005 16h12M9 19.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM20.5 19.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z"></path>
                            </svg>
                        </div>
                        <p class="font-semibold text-gray-800 text-sm">Shopping Cart</p>
                        <p class="text-xs text-gray-600 mt-1">Review items</p>
                    </button>

                    <button
                        @click="router.push('/notifications')"
                        class="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-xl hover:border-orange-200 transition-all duration-200 transform hover:scale-105 group"
                    >
                        <div class="w-12 h-12 bg-gradient-to-br from-purple-100 to-purple-200 rounded-lg flex items-center justify-center mx-auto mb-3 group-hover:from-purple-200 group-hover:to-purple-300 transition-all duration-200">
                            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM10.586 6.414A2 2 0 019.172 6H7a2 2 0 00-2 2v4a2 2 0 002 2h2.172a2 2 0 011.414.586l.414.414a2 2 0 002.828 0l.414-.414A2 2 0 0115.828 14H18a2 2 0 002-2V8a2 2 0 00-2-2h-2.172a2 2 0 01-1.414-.586L15 4.586a2 2 0 00-2.828 0L11.758 5z"></path>
                            </svg>
                        </div>
                        <p class="font-semibold text-gray-800 text-sm">Notifications</p>
                        <p class="text-xs text-gray-600 mt-1">Stay updated</p>
                    </button>
                </div>
            </div>

            <!-- Statistics Dashboard -->
            <div class="mb-8">
                <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
                    <svg class="w-7 h-7 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                    </svg>
                    Your Health Dashboard
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <!-- Total Orders Card -->
                    <div class="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-200">
                        <div class="flex items-center justify-between mb-4">
                            <div class="w-12 h-12 bg-gradient-to-br from-green-100 to-green-200 rounded-xl flex items-center justify-center">
                                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                                </svg>
                            </div>
                            <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full font-medium">
                                All time
                            </span>
                        </div>
                        <div>
                            <p class="text-3xl font-bold text-gray-800 mb-1">5</p>
                            <p class="text-sm font-medium text-gray-600">Total Orders</p>
                            <p class="text-xs text-green-600 mt-2 flex items-center gap-1">
                                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                                </svg>
                                Completed successfully
                            </p>
                        </div>
                    </div>

                    <!-- Notifications Card -->
                    <div class="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-200">
                        <div class="flex items-center justify-between mb-4">
                            <div class="w-12 h-12 bg-gradient-to-br from-red-100 to-red-200 rounded-xl flex items-center justify-center">
                                <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM10.586 6.414A2 2 0 019.172 6H7a2 2 0 00-2 2v4a2 2 0 002 2h2.172a2 2 0 011.414.586l.414.414a2 2 0 002.828 0l.414-.414A2 2 0 0115.828 14H18a2 2 0 002-2V8a2 2 0 00-2-2h-2.172a2 2 0 01-1.414-.586L15 4.586a2 2 0 00-2.828 0L11.758 5z"></path>
                                </svg>
                            </div>
                            <span class="text-xs bg-red-100 text-red-800 px-2 py-1 rounded-full font-medium animate-pulse">
                                New
                            </span>
                        </div>
                        <div>
                            <p class="text-3xl font-bold text-gray-800 mb-1">10</p>
                            <p class="text-sm font-medium text-gray-600">Notifications</p>
                            <p class="text-xs text-red-600 mt-2 flex items-center gap-1">
                                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16c-.77.833.192 2.5 1.732 2.5z"></path>
                                </svg>
                                Requires attention
                            </p>
                        </div>
                    </div>

                    <!-- Pending Deliveries Card -->
                    <div class="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-200">
                        <div class="flex items-center justify-between mb-4">
                            <div class="w-12 h-12 bg-gradient-to-br from-blue-100 to-blue-200 rounded-xl flex items-center justify-center">
                                <svg class="w-6 h-6 text-blue-600 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path>
                                </svg>
                            </div>
                            <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full font-medium">
                                In transit
                            </span>
                        </div>
                        <div>
                            <p class="text-3xl font-bold text-gray-800 mb-1">2</p>
                            <p class="text-sm font-medium text-gray-600">Pending Deliveries</p>
                            <p class="text-xs text-blue-600 mt-2 flex items-center gap-1">
                                <svg class="w-3 h-3 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                                </svg>
                                Being processed
                            </p>
                        </div>
                    </div>

                    <!-- Cart Items Card -->
                    <div class="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-200">
                        <div class="flex items-center justify-between mb-4">
                            <div class="w-12 h-12 bg-gradient-to-br from-yellow-100 to-yellow-200 rounded-xl flex items-center justify-center">
                                <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.293 2.293A1 1 0 005 16h12M9 19.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM20.5 19.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z"></path>
                                </svg>
                            </div>
                            <span class="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full font-medium">
                                70% full
                            </span>
                        </div>
                        <div>
                            <p class="text-3xl font-bold text-gray-800 mb-1">7</p>
                            <p class="text-sm font-medium text-gray-600">Cart Items</p>
                            <p class="text-xs text-yellow-600 mt-2 flex items-center gap-1">
                                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                                Ready for checkout
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recent Activity -->
            <div class="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
                <div class="bg-gradient-to-r from-gray-50 to-blue-50 px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2">
                        <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        Recent Activity
                    </h3>
                    <p class="text-sm text-gray-600 mt-1">Your latest pharmacy interactions</p>
                </div>
                <div class="p-6">
                    <div class="space-y-4">
                        <div class="flex items-center gap-4 p-3 bg-green-50 rounded-lg border border-green-100">
                            <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                                </svg>
                            </div>
                            <div class="flex-1">
                                <p class="font-medium text-gray-800">Order #1234 delivered successfully</p>
                                <p class="text-sm text-gray-600">2 hours ago</p>
                            </div>
                        </div>
                        
                        <div class="flex items-center gap-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
                            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
                                </svg>
                            </div>
                            <div class="flex-1">
                                <p class="font-medium text-gray-800">Added Paracetamol to cart</p>
                                <p class="text-sm text-gray-600">1 day ago</p>
                            </div>
                        </div>
                        
                        <div class="flex items-center gap-4 p-3 bg-orange-50 rounded-lg border border-orange-100">
                            <div class="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center">
                                <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                                </svg>
                            </div>
                            <div class="flex-1">
                                <p class="font-medium text-gray-800">New prescription order placed</p>
                                <p class="text-sm text-gray-600">3 days ago</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-6 text-center">
                        <button
                            @click="router.push('/orders')"
                            class="inline-flex items-center gap-2 text-orange-600 hover:text-orange-700 font-medium transition-colors"
                        >
                            View all activity
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
