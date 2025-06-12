// stores/notification.js
import { defineStore } from "pinia";
import axios from "axios";

export const useNotificationStore = defineStore("notification", {
  state: () => ({
    notifications: [],
    isLoading: false,
    error: null,
    markingAsRead: {},
    role: null, // 'customer' or 'salesperson'
    userId: null,
    polling: null,
    pollingInterval: 30000,
  }),

  getters: {
    allNotifications: (state) => state.notifications,
    unreadNotifications: (state) => state.notifications.filter(n => !n.read),
    readNotifications: (state) => state.notifications.filter(n => n.read),
    unreadCount: (state) => state.unreadNotifications.length,
    getNotificationsByType: (state) => (type) => state.notifications.filter(n => n.type === type),
    recentNotifications: (state) => {
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      return state.notifications
        .filter(n => new Date(n.created_at) > yesterday)
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    },
    hasNotifications: (state) => state.notifications.length > 0,
    hasUnreadNotifications: (state) => state.unreadNotifications.length > 0,
  },

  actions: {
    initialize(role, userId = null) {
      this.role = role;
      this.userId = userId;
      this.fetchNotifications();
      this.startPolling();
    },

    async fetchNotifications() {
      if (!this.role) return;

      this.isLoading = true;
      this.error = null;

      try {
        let endpoint;
        if (this.role === "customer" && this.userId) {
          endpoint = `/api/notifications/customer/${this.userId}/`;
        } else if (this.role === "salesperson") {
          endpoint = `/api/notifications/salesperson/`;
        } else {
          throw new Error("Invalid role or missing user ID");
        }

        const response = await axios.get(endpoint);
        this.notifications = this.sortNotificationsByDate(response.data || []);
      } catch (error) {
        this.error = "Failed to load notifications.";
        console.error(error);
        this.notifications = [];
      } finally {
        this.isLoading = false;
      }
    },

    async markAsRead(notificationId) {
      if (this.markingAsRead[notificationId]) return;

      this.markingAsRead = { ...this.markingAsRead, [notificationId]: true };

      try {
        const res = await axios.patch(`/api/notifications/${notificationId}/mark-as-read/`);
        const index = this.notifications.findIndex(n => n.id === notificationId);
        if (index !== -1) {
          this.notifications[index] = {
            ...this.notifications[index],
            read: true,
            ...res.data,
          };
        }
      } catch (err) {
        this.error = "Failed to mark as read.";
        console.error(err);
      } finally {
        this.markingAsRead = { ...this.markingAsRead, [notificationId]: false };
      }
    },

    async markAllAsRead() {
      try {
        await Promise.all(this.unreadNotifications.map(n => this.markAsRead(n.id)));
      } catch (err) {
        this.error = "Failed to mark all as read.";
      }
    },

    async deleteNotification(notificationId) {
      try {
        await axios.delete(`/api/notifications/${notificationId}/delete/`);
        this.notifications = this.notifications.filter(n => n.id !== notificationId);
      } catch (err) {
        this.error = "Failed to delete notification.";
      }
    },

    async clearAllNotifications() {
      try {
        await Promise.all(this.notifications.map(n => this.deleteNotification(n.id)));
      } catch (err) {
        this.error = "Failed to clear notifications.";
      }
    },

    addNotification(notification) {
      const exists = this.notifications.find(n => n.id === notification.id);
      if (!exists) {
        this.notifications.unshift(notification);
        this.notifications = this.sortNotificationsByDate(this.notifications);
      }
    },

    updateNotification(updatedNotification) {
      const index = this.notifications.findIndex(n => n.id === updatedNotification.id);
      if (index !== -1) {
        this.notifications[index] = { ...this.notifications[index], ...updatedNotification };
      }
    },

    startPolling() {
      if (this.polling) return;
      this.polling = setInterval(() => this.fetchNotifications(), this.pollingInterval);
    },

    stopPolling() {
      if (this.polling) {
        clearInterval(this.polling);
        this.polling = null;
      }
    },

    setPollingInterval(interval) {
      this.pollingInterval = interval;
      this.stopPolling();
      this.startPolling();
    },

    sortNotificationsByDate(notifications) {
      return notifications.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    },

    formatNotificationDate(dateStr) {
      const date = new Date(dateStr);
      const now = new Date();
      const diff = (now - date) / 1000;

      if (diff < 60) return "Just now";
      if (diff < 3600) return `${Math.floor(diff / 60)} minutes ago`;
      if (diff < 86400) return `${Math.floor(diff / 3600)} hours ago`;
      if (diff < 172800) return "Yesterday";
      return date.toLocaleDateString();
    },

    getNotificationIcon(type) {
      const icons = {
        NEW_ORDER: "🛍️",
        ORDER_PROCESSING: "⏳",
        ORDER_DELIVERED: "✅",
        ORDER_CANCELLED: "❌",
        PAYMENT_RECEIVED: "💳",
        STOCK_ALERT: "📦",
        SYSTEM_UPDATE: "🔄",
        PROMOTION: "🎉",
      };
      return icons[type] || "📢";
    },

    getNotificationColor(type) {
      const colors = {
        NEW_ORDER: "blue",
        ORDER_PROCESSING: "orange",
        ORDER_DELIVERED: "green",
        ORDER_CANCELLED: "red",
        PAYMENT_RECEIVED: "purple",
        STOCK_ALERT: "yellow",
        SYSTEM_UPDATE: "gray",
        PROMOTION: "pink",
      };
      return colors[type] || "gray";
    },

    clearError() {
      this.error = null;
    },

    reset() {
      this.stopPolling();
      this.notifications = [];
      this.isLoading = false;
      this.error = null;
      this.markingAsRead = {};
      this.role = null;
      this.userId = null;
    },
  },
});
