<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <!-- Backdrop -->
    <div
      class="fixed inset-0 bg-gray-900/50 backdrop-blur-sm"
      @click="$emit('close')"
    ></div>

    <!-- Modal -->
    <div class="flex min-h-full items-center justify-center p-4">
      <div class="relative bg-white rounded-xl shadow-xl w-full max-w-2xl">
        <!-- Header -->
        <div
          class="flex items-center justify-between p-6 border-b border-gray-200"
        >
          <h3 class="text-lg font-semibold text-gray-900">
            {{ medication ? "Edit Medication" : "Add New Medication" }}
          </h3>
          <button
            @click="$emit('close')"
            class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X class="w-5 h-5 text-gray-500" />
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Name -->
            <BaseInput
              v-model="form.name"
              label="Medication Name"
              placeholder="Enter medication name"
              required
              :error-message="errors.name"
            />

            <!-- Brand -->
            <BaseInput
              v-model="form.brand"
              label="Brand"
              placeholder="Enter brand name"
              :error-message="errors.brand"
            />

            <!-- Category -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Category <span class="text-red-500">*</span>
              </label>
              <select
                v-model="form.category"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                required
              >
                <option value="">Select a category</option>
                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
              <p v-if="errors.category" class="mt-1 text-sm text-red-600">
                {{ errors.category }}
              </p>
            </div>

            <!-- Stock Quantity -->
            <BaseInput
              v-model="form.stock"
              type="number"
              label="Stock Quantity"
              placeholder="Enter quantity"
              required
              :error-message="errors.stock"
            />

            <!-- Price -->
            <div class="md:col-span-2">
              <BaseInput
                v-model="form.price"
                type="number"
                step="0.01"
                label="Price (₵)"
                placeholder="0.00"
                required
                :error-message="errors.price"
              />
            </div>
          </div>

          <!-- Description -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              v-model="form.description"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              placeholder="Enter medication description..."
            ></textarea>
            <p v-if="errors.description" class="mt-1 text-sm text-red-600">
              {{ errors.description }}
            </p>
          </div>

          <!-- Images -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Product Images
            </label>
            <div class="space-y-4">
              <!-- Upload Area -->
              <div
                @drop="handleDrop"
                @dragover.prevent
                @dragenter.prevent
                class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-orange-400 transition-colors"
              >
                <Upload class="w-8 h-8 text-gray-400 mx-auto mb-2" />
                <p class="text-sm text-gray-600">
                  Drag and drop images here, or
                  <label
                    class="text-orange-600 hover:text-orange-700 cursor-pointer font-medium"
                  >
                    browse
                    <input
                      ref="fileInput"
                      type="file"
                      multiple
                      accept="image/*"
                      class="hidden"
                      @change="handleFileSelect"
                    />
                  </label>
                </p>
                <p class="text-xs text-gray-500 mt-1">
                  PNG, JPG, GIF up to 5MB each
                </p>
              </div>

              <!-- Selected Images Preview -->
              <div
                v-if="selectedImages.length > 0"
                class="grid grid-cols-3 gap-4"
              >
                <div
                  v-for="(image, index) in selectedImages"
                  :key="index"
                  class="relative group"
                >
                  <img
                    :src="image.preview"
                    :alt="`Preview ${index + 1}`"
                    class="w-full h-24 object-cover rounded-lg border border-gray-200"
                  />
                  <button
                    type="button"
                    @click="removeImage(index)"
                    class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <X class="w-4 h-4" />
                  </button>
                </div>
              </div>

              <!-- Existing Images (when editing) -->
              <div v-if="medication?.images?.length > 0" class="space-y-2">
                <p class="text-sm font-medium text-gray-700">Current Images:</p>
                <div class="grid grid-cols-3 gap-4">
                  <div
                    v-for="image in medication.images"
                    :key="image.id"
                    class="relative group"
                  >
                    <img
                      :src="`https://techrems.pythonanywhere.com${image.image}`"
                      :alt="medication.name"
                      class="w-full h-24 object-cover rounded-lg border border-gray-200"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div
            class="flex items-center justify-end gap-3 pt-4 border-t border-gray-200"
          >
            <BaseButton type="button" variant="outline" @click="$emit('close')">
              Cancel
            </BaseButton>
            <BaseButton type="submit" :loading="isSubmitting">
              {{ medication ? "Update" : "Add" }} Medication
            </BaseButton>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { computed, ref, reactive, onMounted, watch } from "vue";
  import { X, Upload } from "lucide-vue-next";

  import BaseInput from "@/components/shared/BaseInput.vue";
  import BaseButton from "@/components/shared/BaseButton.vue";

  import { useMedStore } from "@/stores/medStore";

  const props = defineProps({
    medication: {
      type: Object,
      default: null,
    },
  });

  const emit = defineEmits(["close", "saved"]);

  const medStore = useMedStore();

  const form = reactive({
    name: "",
    brand: "",
    category: "",
    price: "",
    stock: "",
    description: "",
  });

  const errors = ref({});
  const isSubmitting = ref(false);
  const selectedImages = ref([]);
  const fileInput = ref(null);

  const categories = computed(() => medStore.categories || []);

  // Populate form when editing
  watch(
    () => props.medication,
    (medication) => {
      if (medication) {
        form.name = medication.name || "";
        form.brand = medication.brand || "";
        form.category = medication.category?.id || "";
        form.price = medication.price || "";
        form.stock = medication.stock || "";
        form.description = medication.description || "";
      }
    },
    { immediate: true }
  );

  const handleFileSelect = (event) => {
    const files = Array.from(event.target.files);
    processFiles(files);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const files = Array.from(event.dataTransfer.files);
    processFiles(files);
  };

  const processFiles = (files) => {
    files.forEach((file) => {
      if (file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (e) => {
          selectedImages.value.push({
            file,
            preview: e.target.result,
          });
        };
        reader.readAsDataURL(file);
      }
    });
  };

  const removeImage = (index) => {
    selectedImages.value.splice(index, 1);
  };

  const validateForm = () => {
    errors.value = {};

    if (!form.name.trim()) {
      errors.value.name = "Medication name is required";
    }

    if (!form.category) {
      errors.value.category = "Category is required";
    }

    if (!form.price || parseFloat(form.price) <= 0) {
      errors.value.price = "Valid price is required";
    }

    if (!form.stock || parseInt(form.stock) < 0) {
      errors.value.stock = "Valid stock quantity is required";
    }

    return Object.keys(errors.value).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    try {
      isSubmitting.value = true;

      const formData = new FormData();
      formData.append("name", form.name);
      formData.append("brand", form.brand);
      formData.append("category", form.category);
      formData.append("price", form.price);
      formData.append("stock", form.stock);
      formData.append("description", form.description);

      // Add images
      selectedImages.value.forEach((image, index) => {
        formData.append(`product_images`, image.file);
      });

      if (props.medication) {
        await medStore.updateProduct(props.medication.id, formData);
      } else {
        await medStore.addProduct(formData);
      }

      emit("saved");
    } catch (error) {
      console.error("Failed to save medication:", error);
      // Handle specific validation errors from backend
      if (error.response?.data) {
        errors.value = error.response.data;
      }
    } finally {
      isSubmitting.value = false;
    }
  };

  onMounted(() => {
    medStore.fetchCategories();
  });
</script>
