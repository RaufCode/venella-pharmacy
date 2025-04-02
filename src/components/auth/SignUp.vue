<script setup>
    import InputField from "@/components/ui/InputField.vue";
    import btn from "@/components/ui/btn.vue";
    import { ref, reactive } from "vue";

    const form = reactive({
        username: "",
        telephone: "",
        email: "",
        password1: "",
        password2: "",
    });
    let formValidation = () => {
        const usernameRegex = /^[A-Za-z]{3,}(-[A-Za-z]{3,})*$/;
        const passwordRegex =
            /^(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?])[A-Za-z\d!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]{8,}$/;
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        const telephoneRegex = /^\+?[0-9\s\-()]{10,15}$/;

        try {
            if (!usernameRegex.test(form.username))
                throw "Username must be 3-20 characters long and can't contain special character except hyphen";
            if (!telephoneRegex.test(form.telephone))
                throw "Telephone number must be 10-15 digits and may include spaces, dashes, or parentheses";
            if (!emailRegex.test(form.email)) throw "Invalid email format";
            if (!passwordRegex.test(form.password1))
                throw "Password must be at least 6 characters long and include one special character";
            if (form.password1 !== form.password2)
                throw "passwords do not match";
            errorMsg = "successful";
        } catch (error) {
            errorMsg.value = error;
        }
    };
</script>
<template>
    <div class="flex lg:h-screen lg:w-screen">
        <div
            class="w-screen min-h-screen flex justify-center items-center lg:w-1/2"
        >
            <form
                @submit.prevent="formValidation"
                method="post"
                class="max-w-[370px] p-5 shadow w-11/12 mx-auto"
            >
                <h1 class="form-title">Sign up</h1>
                <InputField v-model="form.username" labelname="First Name" />
                <InputField v-model="form.username" labelname="Last Name" />
                <InputField
                    v-model="form.telephone"
                    labelname="Telephone"
                    type="tel"
                />
                <InputField
                    v-model="form.email"
                    labelname="Email"
                    type="email"
                />
                <InputField
                    v-model="form.password1"
                    labelname="Password"
                    type="password"
                />
                <InputField
                    v-model="form.password2"
                    labelname="Confirm password"
                    type="password"
                />
                <btn btnName="Sign up" />
                <p class="mt-3 text-sm text-gray-700">
                    Already have an account?
                    <a href="/sign-in" class="text-orange-700 text-xs"
                        >Sign in</a
                    >
                </p>
            </form>
        </div>
        <div
            class="hidden lg:flex items-center justify-center lg:w-1/2 lg:h-full bg-orange-700"
        >
            <h1 class="text-5xl font-styleScript text-white">
                Vanella Pharmacy
            </h1>
        </div>
    </div>
</template>
