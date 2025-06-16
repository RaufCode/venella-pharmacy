<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <!-- Backdrop -->
    <div
      class="fixed inset-0 bg-gray-900/50 backdrop-blur-sm"
      @click="$emit('close')"
    ></div>

    <!-- Modal -->
    <div class="flex min-h-full items-center justify-center p-4">
      <div class="relative bg-white rounded-xl shadow-xl w-full max-w-lg">
        <!-- Header -->
        <div
          class="flex items-center justify-between p-6 border-b border-gray-200"
        >
          <h3 class="text-lg font-semibold text-gray-900">
            {{ staff ? "Edit Staff Member" : "Add New Staff Member" }}
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
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- First Name -->
            <BaseInput
              v-model="form.first_name"
              label="First Name"
              placeholder="Enter first name"
              required
              :error-message="errors.first_name"
            />

            <!-- Last Name -->
            <BaseInput
              v-model="form.last_name"
              label="Last Name"
              placeholder="Enter last name"
              required
              :error-message="errors.last_name"
            />
          </div>

          <!-- Other Names -->
          <BaseInput
            v-model="form.other_names"
            label="Other Names"
            placeholder="Enter other names (optional)"
            :error-message="errors.other_names"
          />

          <!-- Email -->
          <BaseInput
            v-model="form.email"
            type="email"
            label="Email Address"
            placeholder="Enter email address"
            required
            :error-message="errors.email"
          />

          <!-- Phone -->
          <BaseInput
            v-model="form.phone"
            type="tel"
            label="Phone Number"
            placeholder="Enter phone number"
            required
            :error-message="errors.phone"
          />

          <!-- Address -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Address <span class="text-red-500">*</span>
            </label>
            <textarea
              v-model="form.address"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              placeholder="Enter full address..."
              required
            ></textarea>
            <p v-if="errors.address" class="mt-1 text-sm text-red-600">
              {{ errors.address }}
            </p>
          </div>

          <!-- Role Info -->
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div class="flex items-center gap-2">
              <Info class="w-5 h-5 text-blue-600" />
              <span class="text-sm font-medium text-blue-900"
                >Role Information</span
              >
            </div>
            <p class="text-sm text-blue-700 mt-1">
              This staff member will be assigned the "Salesperson" role with
              access to medication and order management.
            </p>
          </div>

          <!-- Actions -->
          <div
            class="flex items-center justify-end gap-3 pt-4 border-t border-gray-200"
          >
            <BaseButton type="button" variant="outline" @click="$emit('close')">
              Cancel
            </BaseButton>
            <BaseButton type="submit" :loading="isSubmitting">
              {{ staff ? "Update" : "Add" }} Staff Member
            </BaseButton>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, reactive, watch } from "vue";
  import { X, Info } from "lucide-vue-next";

  import BaseInput from "@/components/shared/BaseInput.vue";
  import BaseButton from "@/components/shared/BaseButton.vue";

  import axios from "axios";

  const props = defineProps({
    staff: {
      type: Object,
      default: null,
    },
  });

  const emit = defineEmits(["close", "saved"]);

  const form = reactive({
    first_name: "",
    last_name: "",
    other_names: "",
    email: "",
    phone: "",
    address: "",
  });

  const errors = ref({});
  const isSubmitting = ref(false);

  // Populate form when editing
  watch(
    () => props.staff,
    (staff) => {
      if (staff) {
        form.first_name = staff.profile.first_name || "";
        form.last_name = staff.profile.last_name || "";
        form.other_names = staff.profile.other_names || "";
        form.email = staff.email || "";
        form.phone = staff.profile.phone || "";
        form.address = staff.profile.address || "";
        // Don't populate password for existing staff
      }
    },
    { immediate: true }
  );

  const validateForm = () => {
    errors.value = {};

    if (!form.first_name.trim()) {
      errors.value.first_name = "First name is required";
    }

    if (!form.last_name.trim()) {
      errors.value.last_name = "Last name is required";
    }

    if (!form.email.trim()) {
      errors.value.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(form.email)) {
      errors.value.email = "Email format is invalid";
    }

    if (!form.phone.trim()) {
      errors.value.phone = "Phone number is required";
    }

    if (!form.address.trim()) {
      errors.value.address = "Address is required";
    }

    return Object.keys(errors.value).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    try {
      isSubmitting.value = true;

      const data = {
        first_name: form.first_name.trim(),
        last_name: form.last_name.trim(),
        other_names: form.other_names.trim(),
        email: form.email.trim().toLowerCase(),
        phone: form.phone.trim(),
        address: form.address.trim(),
        role: "salesperson",
      };

      // Only include password for new staff
      if (!props.staff) {
        data.password = form.password;
      }

      if (props.staff) {
        await axios.put(
          `/api/core/accounts/salespersons/${props.staff.id}/`,
          data
        );
      } else {
        await axios.post("/api/core/accounts/salesperson/create/", data);
      }

      emit("saved");
    } catch (error) {
      console.error("Failed to save staff:", error);
      // Handle specific validation errors from backend
      if (error.response?.data) {
        errors.value = error.response.data;
      }
    } finally {
      isSubmitting.value = false;
    }
  };
</script>
