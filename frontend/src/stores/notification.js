import { defineStore } from "pinia";
import axios from "axios";
import axiosInstance from "@/services/api"; // adjust path as needed
import { useAuthStore } from "./auth"; // adjust path as needed
import { useToast } from "vue-toastification";

export const useNotificationStore = defineStore("notification", {
  state: () => ({
    notifications: [],
    isLoading: false,
    error: null,
    pollInterval: null,
  }),

  getters: {
    unreadCount(state) {
      return state.notifications.filter((n) => !n.read).length;
    },
    sortedNotifications(state) {
      return [...state.notifications].sort(
        (a, b) => new Date(b.created_at) - new Date(a.created_at)
      );
    },
  },

  actions: {
    async fetchNotifications() {
      const toast = useToast();
      const authStore = useAuthStore();
      const userId = authStore.user?.id;
      const role = authStore.user?.role;

    
      this.isLoading = true;
      this.error = null;

      try {
        let url = "";
        if (role === "customer") {
          url = `/api/notifications/customer/${userId}/`;
        } else if (role === "salesperson" || role === "admin") {
          url = `/api/notifications/sales-person/`;
        } else {
          throw new Error("Invalid user role");
        }
        const response = await axiosInstance.get(url);
        this.notifications = response.data || [];
      } catch (err) {
        this.notifications = [];
      } finally {
        this.isLoading = false;
      }
    },

    async markAsRead(notificationId) {
      const toast = useToast();
      try {
        await axiosInstance.put(`/api/notifications/${notificationId}/mark-as-read/`);
        const index = this.notifications.findIndex((n) => n.id === notificationId);
        if (index !== -1) {
          this.notifications[index].read = true;
        }
      } catch (err) {
        toast.error(`Failed to mark notification as read.`);
      }
    },

    async deleteNotification(notificationId) {
      const toast = useToast();
      try {
        await axiosInstance.delete(`/api/notifications/${notificationId}/delete/`);
        this.notifications = this.notifications.filter(
          (n) => n.id !== notificationId
        );
        toast.success("Notification deleted.");
      } catch (err) {
        toast.error("Failed to delete notification.");
        this.error = "Failed to delete notification.";
      }
    },

    startPolling() {
      this.stopPolling(); // clear existing interval
      this.fetchNotifications();
      this.pollInterval = setInterval(() => {
        this.fetchNotifications();
      }, 30000);
    },

    stopPolling() {
      if (this.pollInterval) {
        clearInterval(this.pollInterval);
        this.pollInterval = null;
      }
    },
  },
});
