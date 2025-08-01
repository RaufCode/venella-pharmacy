// src/stores/orderStore.js
import { defineStore } from 'pinia'
import axios from 'axios'
import axiosInstance from '@/services/api' // adjust path as needed
import { useToast } from "vue-toastification";

export const useOrderStore = defineStore('orderStore', {
  state: () => ({
    orders: [],
    customerOrders: [],
    orderDetails: null,
    loading: false,
    error: null,
    successMessage: null,
    searchDate: null,
    // Add pendingOrder to store order payload before payment
    pendingOrder: null,
    pendingAmount: null,
  }),

  getters: {
    pendingOrders: (state) =>
      Array.isArray(state.orders) ? state.orders.filter(order => order.status === 'pending') : [],
    processingOrders: (state) =>
      Array.isArray(state.orders) ? state.orders.filter(order => order.status === 'processing') : [],
    completedOrders: (state) =>
      Array.isArray(state.orders) ? state.orders.filter(order => order.status === 'completed') : [],
    cancelledOrders: (state) =>
      Array.isArray(state.orders) ? state.orders.filter(order => order.status === 'cancelled') : [],

    sumOrdersAmount: () => (ordersList) =>
      Array.isArray(ordersList)
        ? ordersList.reduce((sum, order) => sum + parseFloat(order.totalAmount || 0), 0)
        : 0,

    totalRevenue(state) {
      return this.sumOrdersAmount(this.completedOrders)
    },

    monthlyRevenue(state) {
      const now = new Date()
      return this.sumOrdersAmount(
        this.completedOrders.filter(order => {
          const d = new Date(order.date)
          return d.getMonth() === now.getMonth() && d.getFullYear() === now.getFullYear()
        })
      )
    },

    dailyRevenue(state) {
      const now = new Date()
      return this.sumOrdersAmount(
        this.completedOrders.filter(order => {
          const d = new Date(order.date)
          return (
            d.getDate() === now.getDate() &&
            d.getMonth() === now.getMonth() &&
            d.getFullYear() === now.getFullYear()
          )
        })
      )
    },

    searchedRevenue(state) {
      if (!state.searchDate) return 0
      const search = new Date(state.searchDate)
      return this.sumOrdersAmount(
        this.completedOrders.filter(order => {
          const d = new Date(order.date)
          return (
            d.getDate() === search.getDate() &&
            d.getMonth() === search.getMonth() &&
            d.getFullYear() === search.getFullYear()
          )
        })
      )
    }
  },

  actions: {
    async fetchAllOrders() {
      const toast = useToast();
      this.loading = true
      this.error = null
      try {
        const res = await axiosInstance.get('/api/orders/')
        this.orders.splice(0, this.orders.length, ...(res.data || []))
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to load orders.'
        toast.error(this.error);
      } finally {
        this.loading = false
      }
    },

    async fetchPendingOrders() {
      const toast = useToast();
      this.loading = true
      this.error = null
      try {
        const res = await axiosInstance.get('/api/orders/pending/')
        this.orders.splice(0, this.orders.length, ...(res.data || []))
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to load pending orders.'
        toast.error(this.error);
      } finally {
        this.loading = false
      }
    },

    async fetchProcessingOrders() {
      const toast = useToast();
      this.loading = true
      this.error = null
      try {
        const res = await axiosInstance.get('/api/orders/processing/')
        this.orders.splice(0, this.orders.length, ...(res.data || []))
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to load processing orders.'
        toast.error(this.error);
      } finally {
        this.loading = false
      }
    },

    async fetchCustomerOrders() {
      const toast = useToast();
      this.loading = true
      this.error = null
      try {
        const res = await axiosInstance.get('/api/orders/customer/orders/')
        this.customerOrders = res.data || []
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to fetch your orders.'
        toast.error(this.error);
      } finally {
        this.loading = false
      }
    },

    async fetchOrderDetails(orderId) {
      const toast = useToast();
      this.loading = true
      this.error = null
      try {
        const res = await axiosInstance.get(`/api/orders/${orderId}/retrieve/`)
        this.orderDetails = res.data
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to retrieve order details.'
        toast.error(this.error);
      } finally {
        this.loading = false
      }
    },

    // async createOrder(payload) {
    //   const toast = useToast();
    //   this.loading = true
    //   this.error = null
    //   try {
    //     await axiosInstance.post('/api/orders/create/', payload)
    //     this.successMessage = 'Order created successfully.'
    //     toast.success(this.successMessage);
    //     await this.fetchCustomerOrders()
    //   } catch (err) {
    //     this.error = err.response?.data?.message || 'Order creation failed.'
    //     toast.error(this.error);
    //   } finally {
    //     this.loading = false
    //   }
    // },

    async deleteOrder(orderId) {
      const toast = useToast();
      this.loading = true
      this.error = null
      try {
        await axiosInstance.delete(`/api/orders/${orderId}/delete/`)
        this.successMessage = 'Order deleted successfully.'
        toast.success(this.successMessage);
        await this.fetchAllOrders()
        await this.fetchCustomerOrders()
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to delete order.'
        toast.error(this.error);
      } finally {
        this.loading = false
      }
    },

    async updateOrderStatus(orderId, newStatus) {
      const toast = useToast();
      this.loading = true
      this.error = null
      try {
        await axiosInstance.put(`/api/orders/${orderId}/update-status/`, { status: newStatus })
        this.successMessage = 'Order status updated.'
        toast.success(this.successMessage);
        await this.fetchAllOrders()
        await this.fetchCustomerOrders()
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to update order status.'
        toast.error(this.error);
      } finally {
        this.loading = false
      }
    },

    setSearchDate(date) {
      this.searchDate = date
    },

    setPendingOrder({ order, amount }) {
      this.pendingOrder = order;
      this.pendingAmount = amount;
    },
    clearPendingOrder() {
      this.pendingOrder = null;
      this.pendingAmount = null;
    },

    clearMessages() {
      this.error = null
      this.successMessage = null
    }
  }
})