<template>
    <div class="flex items-center justify-center h-32 bg-white">
        <div class="flex space-x-2 relative">
            <span
                class="w-3 h-3 bg-orange-500 rounded-full animate-[dotMove_1.2s_infinite] [animation-delay:0s]"
            ></span>
            <span
                class="w-3 h-3 bg-orange-500 rounded-full animate-[dotMove_1.2s_infinite] [animation-delay:0.2s]"
            ></span>
            <span
                class="w-3 h-3 bg-orange-500 rounded-full animate-[dotMove_1.2s_infinite] [animation-delay:0.4s]"
            ></span>
        </div>
    </div>
</template>

<style>
    @keyframes dotMove {
        0% {
            transform: translateX(0);
            opacity: 0.3;
        }
        25% {
            transform: translateX(4px);
            opacity: 0.6;
        }
        50% {
            transform: translateX(8px);
            opacity: 1;
        }
        75% {
            transform: translateX(12px);
            opacity: 0.6;
        }
        100% {
            transform: translateX(16px);
            opacity: 0;
        }
    }
</style>
