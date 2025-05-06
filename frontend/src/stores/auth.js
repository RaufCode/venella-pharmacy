import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router"; // Import Vue Router

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: localStorage.getItem("token") || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    getUser: (state) => state.user,
    getUserRole: (state) => state.user?.role || "guest",
  },

  actions: {
    async login(credentials) {
      try {
        const response = await axios.post("/api/core/auth/login/", credentials);
        this.token = response.data.token;
        this.user = response.data.user;
        localStorage.setItem("token", this.token);
        axios.defaults.headers.common["Authorization"] = `Bearer ${this.token}`;

        if (this.user.role === "admin") {
          router.push("/dashboard"); // Redirect to admin dashboard
        } else if (this.user.role === "salesperson") {
          router.push("/salesperson-dashboard"); // Redirect to pharmacist dashboard
        } else {
          router.push("/customer-dashboard"); // Redirect to customer dashboard
        }
      } catch (error) {
        throw new Error(error.response?.data?.message || "Login failed");
      }
    },

    async register(credentials) {
      try {
        await axios.post("/api/core/accounts/create/", credentials);
        router.push("/login"); // Redirect after registration
      } catch (error) {
        throw new Error(error.response?.data?.message || "Registration failed");
      }
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("token");
      delete axios.defaults.headers.common["Authorization"];

      router.push("/login"); // Redirect after logout
    },
  },
});
