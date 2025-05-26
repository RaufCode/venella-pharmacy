// stores/auth.js
import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: null,
    refreshToken: null,
    user: null,
    ready: false,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    getUser: (state) => state.user,
    getUserRole: (state) => state.user?.role || "guest",
  },
  actions: {
    setToken(accessToken, refreshToken = null) {
      this.token = accessToken;
      this.refreshToken = refreshToken;

      if (accessToken) {
        localStorage.setItem("token", accessToken);
        axios.defaults.headers.common["Authorization"] = `Bearer ${accessToken}`;
      } else {
        localStorage.removeItem("token");
        delete axios.defaults.headers.common["Authorization"];
      }

      if (refreshToken) {
        localStorage.setItem("refreshToken", refreshToken);
      } else {
        localStorage.removeItem("refreshToken");
      }
    },

    setUser(newUser) {
      this.user = newUser;
      if (newUser) {
        localStorage.setItem("user", JSON.stringify(newUser));
      } else {
        localStorage.removeItem("user");
      }
    },

    initializeAuth() {
      const savedToken = localStorage.getItem("token");
      const savedRefresh = localStorage.getItem("refreshToken");
      const savedUser = localStorage.getItem("user");

      if (savedToken) {
        this.token = savedToken;
        axios.defaults.headers.common["Authorization"] = `Bearer ${savedToken}`;
      }

      if (savedRefresh) {
        this.refreshToken = savedRefresh;
      }

      if (savedUser) {
        try {
          this.setUser(JSON.parse(savedUser));
        } catch (e) {
          console.error("Invalid saved user");
          this.setUser(null);
        }
      }

      this.ready = true;
    },

    // ** Register function added here before login **
    async register(registrationData) {
      try {
        const response = await axios.post("/api/core/accounts/create/", registrationData);
        console.log("Register response:", response.data);
        // Optionally redirect to login or automatically login here
        await router.push("/login");
        return response.data;
      } catch (error) {
        console.error("Register error:", error);
        const message = error.response?.data?.message || error.message || "Registration failed";
        throw new Error(message);
      }
    },

    async login(credentials) {
      try {
        const response = await axios.post("/api/core/auth/login/", credentials);
        console.log("Login response data:", response.data);

        const accessToken = response.data.token?.access;
        const refreshToken = response.data.token?.refresh;
        const userData = response.data.user;

        if (!accessToken || !userData) {
          console.warn("Missing accessToken or userData:", { accessToken, userData });
          throw new Error("Invalid login response");
        }

        this.setToken(accessToken, refreshToken);
        this.setUser(userData);

        if (userData.role === "admin") await router.push("/dashboard");
        else if (userData.role === "customer") await router.push("/");
        else await router.push("/salesperson");

      } catch (error) {
        console.error("Login error:", error);
        const message = error.response?.data?.message || error.message || "Login failed";
        throw new Error(message);
      }
    },

    async refreshAccessToken() {
      if (!this.refreshToken) {
        this.logout();
        throw new Error("No refresh token available.");
      }

      try {
        const res = await axios.post("/api/core/auth/refresh/", {
          refresh: this.refreshToken,
        });

        const newAccessToken = res.data.access;
        if (!newAccessToken) {
          throw new Error("Refresh failed");
        }

        this.setToken(newAccessToken, this.refreshToken);
        return newAccessToken;
      } catch (e) {
        this.logout();
        throw new Error("Session expired. Please log in again.");
      }
    },

    logout() {
      this.setToken(null, null);
      this.setUser(null);
      router.push("/login");
    },
  },
});
