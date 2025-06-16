import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from "./auth"; // adjust path as needed

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
      const authStore = useAuthStore();
      const userId = authStore.user?.id;
      const role = authStore.user?.role;

      if (!userId || !role) {
        console.warn("User ID or role missing");
        return;
      }

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

        const response = await axios.get(url);
        this.notifications = response.data || [];
      } catch (err) {
        console.error("Notification fetch error:", err);
        this.error = "Failed to fetch notifications.";
        this.notifications = [];
      } finally {
        this.isLoading = false;
      }
    },

    async markAsRead(notificationId) {
      try {
        await axios.put(`/api/notifications/${notificationId}/mark-as-read/`);
        const index = this.notifications.findIndex((n) => n.id === notificationId);
        if (index !== -1) {
          this.notifications[index].read = true;
        }
      } catch (err) {
        console.error(`Error marking notification ${notificationId} as read`, err);
      }
    },

    async deleteNotification(notificationId) {
      try {
        await axios.delete(`/api/notifications/${notificationId}/delete/`);
        this.notifications = this.notifications.filter(
          (n) => n.id !== notificationId
        );
      } catch (err) {
        console.error(`Error deleting notification ${notificationId}`, err);
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
