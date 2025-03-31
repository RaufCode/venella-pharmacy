<script setup></script>

<template>
    <div class="min-h-screen bg-gray-100">
        <!-- Header -->
        <header
            class="bg-blue-600 text-white p-4 flex justify-between items-center"
        >
            <div class="text-xl font-bold">My Pharmacy</div>
            <nav>
                <ul class="flex space-x-4">
                    <li><a href="#" class="hover:text-blue-200">Home</a></li>
                    <li>
                        <a href="#" class="hover:text-blue-200"
                            >Prescriptions</a
                        >
                    </li>
                    <li><a href="#" class="hover:text-blue-200">Orders</a></li>
                    <li><a href="#" class="hover:text-blue-200">Profile</a></li>
                </ul>
            </nav>
            <div class="text-sm">Welcome, John Doe!</div>
        </header>

        <!-- Main Content -->
        <main class="p-6">
            <!-- Prescription Management -->
            <section class="mb-8">
                <h2 class="text-2xl font-semibold text-blue-600 mb-4">
                    Prescriptions
                </h2>
                <div class="space-y-4">
                    <div class="bg-white p-4 rounded-lg shadow">
                        <h3 class="text-lg font-medium">Medication A</h3>
                        <p>Dosage: 500mg</p>
                        <p>Refills Left: 2</p>
                        <button
                            class="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                        >
                            Request Refill
                        </button>
                    </div>
                    <div class="bg-white p-4 rounded-lg shadow">
                        <h3 class="text-lg font-medium">Medication B</h3>
                        <p>Dosage: 250mg</p>
                        <p>Refills Left: 0</p>
                        <button
                            class="mt-2 px-4 py-2 bg-gray-400 text-white rounded cursor-not-allowed"
                            disabled
                        >
                            No Refills Left
                        </button>
                    </div>
                </div>
            </section>

            <!-- Medication Reminders -->
            <section class="mb-8">
                <h2 class="text-2xl font-semibold text-blue-600 mb-4">
                    Medication Reminders
                </h2>
                <div class="space-y-4">
                    <div class="bg-white p-4 rounded-lg shadow">
                        <h3 class="text-lg font-medium">Medication A</h3>
                        <p>Next Dose: 8:00 AM</p>
                        <button
                            class="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                        >
                            Snooze
                        </button>
                    </div>
                </div>
            </section>

            <!-- Order Tracking -->
            <section>
                <h2 class="text-2xl font-semibold text-blue-600 mb-4">
                    Order Tracking
                </h2>
                <div class="space-y-4">
                    <div class="bg-white p-4 rounded-lg shadow">
                        <h3 class="text-lg font-medium">Order #12345</h3>
                        <p>Status: Shipped</p>
                        <p>Estimated Delivery: October 30, 2023</p>
                    </div>
                </div>
            </section>
        </main>

        <!-- Footer -->
        <footer class="bg-gray-800 text-white text-center p-4">
            <p>Contact Us: (123) 456-7890 | email@pharmacy.com</p>
            <p>
                Follow Us:
                <a href="#" class="text-blue-400 hover:text-blue-300"
                    >Facebook</a
                >
                |
                <a href="#" class="text-blue-400 hover:text-blue-300"
                    >Twitter</a
                >
            </p>
        </footer>
    </div>
</template>
