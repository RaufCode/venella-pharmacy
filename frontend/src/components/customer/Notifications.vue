<template>
    <div
        class="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-gray-100"
    >
        <!-- Topbar -->
        <div
            class="bg-white/80 backdrop-blur-sm shadow-lg border-b border-white/20 sticky top-0 z-40"
        >
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex items-center justify-between h-20">
                    <div class="flex items-center space-x-4">
                        <div class="flex items-center space-x-3">
                            <div
                                class="w-10 h-10 rounded-xl flex items-center justify-center"
                            >
                                <i class="pi pi-bell text-2xl text-gray-700">
                                </i>
                            </div>
                            <div>
                                <h1 class="text-2xl font-bold text-orange-600">
                                    Notifications
                                </h1>
                                <p class="text-sm text-gray-600">
                                    Stay updated with your activities
                                </p>
                            </div>
                        </div>
                        <div class="hidden sm:flex items-center space-x-2">
                            <span
                                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800"
                            >
                                <!-- Placeholder for unread count -->
                                unreadCount
                            </span>
                        </div>
                    </div>
                    <button
                        class="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-xl hover:bg-blue-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                    >
                        Mark all as read
                    </button>
                </div>
            </div>
        </div>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div class="flex flex-col lg:flex-row gap-8">
                <!-- Filters Sidebar (desktop) -->
                <div class="lg:w-72 flex-shrink-0 hidden lg:block">
                    <div
                        class="bg-white/60 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6 sticky top-28"
                    >
                        <h3
                            class="font-bold text-gray-800 mb-6 flex items-center text-lg"
                        >
                            <i class="pi pi-bell h-5 w-5 mr-3 text-blue-500">
                            </i>
                            Filters
                        </h3>
                        <div class="relative mb-6">
                            <i
                                class="pi pi-bell h-5 w-5 mr-3 text-blue-500"
                            ></i>
                            <input
                                placeholder="Search notifications..."
                                class="w-full pl-12 pr-4 py-3 bg-white/70 border border-gray-200 rounded-xl focus:bg-white focus:border-blue-400 focus:ring-4 focus:ring-blue-100 transition-all duration-300 text-sm"
                            />
                        </div>
                        <div class="space-y-2">
                            <!-- Filter options placeholder -->
                        </div>
                    </div>
                </div>

                <!-- Accordion Filter (mobile/tablet) -->
                <div class="lg:hidden">
                    <button
                        class="flex items-center justify-between w-full px-5 py-4 bg-white/60 backdrop-blur-sm border border-white/20 rounded-2xl shadow-lg text-sm font-medium text-gray-700"
                    >
                        <span class="flex items-center">
                            <i
                                class="pi pi-bell h-5 w-5 mr-3 text-blue-500"
                            ></i>
                            Filters & Search
                        </span>
                        <i class="pi pi-bell h-5 w-5 mr-3 text-blue-500"></i>
                    </button>
                </div>

                <!-- Notification List -->
                <div class="flex-1">
                    <div
                        class="bg-white/60 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-12 text-center"
                    >
                        <div
                            class="w-20 h-20 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto mb-6"
                        >
                            <i
                                class="pi pi-bell h-5 w-5 mr-3 text-blue-500"
                            ></i>
                        </div>
                        <h3 class="text-xl font-bold text-gray-800 mb-3">
                            No notifications found
                        </h3>
                        <p class="text-gray-600 text-lg">
                            You're all caught up! Check back later for updates.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
