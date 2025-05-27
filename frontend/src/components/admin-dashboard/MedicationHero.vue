<script setup>
    import { ref, reactive } from "vue";
    import InputField from "@/components/ui/InputField.vue";
    import Btn from "@/components/ui/Btn.vue";
    import axios from "axios";

    // Modal visibility
    const showModal = ref(false);

    // Submission state
    const isSubmitting = ref(false);

    // Form data
    const form = reactive({
        name: "",
        stock: null,
        price: null,
        category: "",
        description: "",
        product_images: [],
    });

    // Handle image uploads
    function handleImageUpload(event) {
        const files = event.target.files;
        if (files && files.length > 0) {
            Array.from(files).forEach((file) => {
                let img = {};
                img["image"] = file;
                form.product_images.push(img);
            });
            console.log("Uploaded images:", form.product_images);
            // form.product_images = Array.from(files);
        }
    }

    // Clear form fields
    function resetForm() {
        form.name = "";
        form.stock = null;
        form.price = null;
        form.category = "";
        form.description = "";
        form.product_images = [];
    }

    // Handle form submission
    async function submitForm() {
        if (
            !form.name ||
            !form.stock ||
            !form.price ||
            !form.category ||
            !form.description ||
            form.product_images.length === 0
        ) {
            alert(
                "Please fill all required fields and upload at least one image."
            );
            return;
        }

        isSubmitting.value = true;

        try {
            const formData = new FormData();
            formData.append("name", form.name);
            formData.append("stock", form.stock);
            formData.append("price", form.price);
            formData.append("category", form.category);
            formData.append("description", form.description);
            formData.append("product_images", form.product_images);

            // 👇 Correctly append all images
            // form.product_images.forEach((image) => {
            //     formData.append("product_images", image);
            // });

            await axios.post("/api/products/add/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });

            alert("Medication added successfully!");
            resetForm();
            showModal.value = false;
        } catch (error) {
            console.error("Error submitting form:", error);
            alert("An error occurred while submitting the form.");
        } finally {
            isSubmitting.value = false;
        }
    }
</script>

<template>
    <div class="h-screen relative flex flex-col flex-1 overflow-hidden">
        <!-- Top bar (Desktop) -->
        <div
            class="hidden w-full md:absolute top-0 z-40 bg-gray-900 md:flex justify-between items-center p-3"
        >
            <h1 class="text-gray-300 text-lg font-styleScript md:text-2xl">
                Inventory Hub
            </h1>
            <button
                @click="showModal = true"
                class="py-2 px-4 bg-orange-600 text-sm text-white font-medium hover:bg-orange-500"
            >
                Add Med
            </button>
        </div>

        <!-- Main content -->
        <div class="overflow-auto overscroll-contain w-full">
            <div class="mx-auto container p-3">
                <!-- Add button (Mobile) -->
                <button
                    @click="showModal = true"
                    class="md:hidden py-2 px-4 bg-orange-600 text-sm text-white font-medium hover:bg-orange-500"
                >
                    Add Med
                </button>

                <!-- Modal -->
                <div
                    v-if="showModal"
                    class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
                >
                    <div class="w-full p-3">
                        <form
                            @submit.prevent="submitForm"
                            class="w-full max-w-xl max-h-[90vh] overflow-y-auto p-4 shadow mx-auto bg-white rounded"
                        >
                            <!-- Modal header -->
                            <div class="flex justify-between items-center mb-4">
                                <h1 class="text-lg font-bold text-gray-800">
                                    Add Meds
                                </h1>
                                <button
                                    type="button"
                                    @click="showModal = false"
                                    class="text-orange-600 text-xl"
                                >
                                    <i class="pi pi-times"></i>
                                </button>
                            </div>

                            <!-- Row 1 -->
                            <div class="md:flex gap-4">
                                <InputField
                                    v-model="form.name"
                                    labelname="Medicine Name"
                                    class="flex-1"
                                    required
                                />
                                <InputField
                                    v-model.number="form.stock"
                                    labelname="Quantity"
                                    type="number"
                                    class="flex-1"
                                    required
                                />
                            </div>

                            <!-- Row 2 -->
                            <div class="md:flex gap-4 mt-3">
                                <InputField
                                    v-model.number="form.price"
                                    labelname="Price"
                                    class="flex-1"
                                    required
                                />
                                <label
                                    class="flex-1 text-sm text-gray-900 block mt-3"
                                >
                                    Category
                                    <select
                                        v-model="form.category"
                                        class="mt-1 w-full border border-gray-400 rounded outline-none focus:border-orange-700 h-9 px-4 md:h-10 bg-transparent"
                                        required
                                    >
                                        <option value="" disabled>
                                            Select Category
                                        </option>
                                        <option
                                            value="11111111-1111-1111-1111-111111111111"
                                        >
                                            Antibiotic
                                        </option>
                                        <option
                                            value="22222222-2222-2222-2222-222222222222"
                                        >
                                            Painkiller
                                        </option>
                                        <option
                                            value="33333333-3333-3333-3333-333333333333"
                                        >
                                            Antihistamine
                                        </option>
                                        <option
                                            value="44444444-4444-4444-4444-444444444444"
                                        >
                                            Supplement
                                        </option>
                                        <option
                                            value="55555555-5555-5555-5555-555555555555"
                                        >
                                            Analgesic
                                        </option>
                                        <option
                                            value="66666666-6666-6666-6666-666666666666"
                                        >
                                            Antacid
                                        </option>
                                        <option
                                            value="77777777-7777-7777-7777-777777777777"
                                        >
                                            Antidepressant
                                        </option>
                                        <option
                                            value="88888888-8888-8888-8888-888888888888"
                                        >
                                            Antiviral
                                        </option>
                                        <option
                                            value="99999999-9999-9999-9999-999999999999"
                                        >
                                            Diuretic
                                        </option>
                                        <option
                                            value="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
                                        >
                                            Vitamin
                                        </option>
                                    </select>
                                </label>
                            </div>

                            <!-- Row 3 -->
                            <div class="mt-3">
                                <label
                                    for="description"
                                    class="block text-sm text-gray-900 mb-1"
                                    >Description</label
                                >
                                <textarea
                                    id="description"
                                    v-model="form.description"
                                    required
                                    rows="2"
                                    class="w-full border border-gray-400 rounded outline-none focus:border-orange-700 px-4 py-2 resize-none"
                                ></textarea>
                            </div>

                            <!-- Image Upload -->
                            <label class="block mt-3 text-sm text-gray-900">
                                Medicine Image
                                <input
                                    type="file"
                                    multiple
                                    @change="handleImageUpload"
                                    class="block mt-1 py-2 w-full border border-gray-400 rounded outline-none focus:border-orange-700 px-4 bg-transparent"
                                    accept="image/*"
                                />
                            </label>

                            <!-- Submit Button -->
                            <div class="mt-5">
                                <Btn :disabled="isSubmitting" btnName="Save" />
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
