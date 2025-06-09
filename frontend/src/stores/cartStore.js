import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";

export const useCartStore = defineStore("cart", {
  state: () => ({
    carts: [],
    isLoading: false,
    error: null,
    cartLoading: {}, // Track loading state per productId
  }),

  getters: {
    cartCount: (state) => state.carts.length,
    subtotal: (state) => {
      return state.carts
        .reduce((total, item) => {
          const price = parseFloat(item?.product?.price || 0);
          const qty = parseInt(item?.quantity || 0);
          return total + (isNaN(price) || isNaN(qty) ? 0 : price * qty);
        }, 0)
        .toFixed(2);
    },
  },

  actions: {
    async fetchCartItems() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await axios.get("/api/carts/customer/cart-items/");
        this.carts = response.data || [];
      } catch (err) {
        console.error("Fetch error:", err);
        this.error = "Failed to load cart items.";
        this.carts = [];
      } finally {
        this.isLoading = false;
      }
    },

    async addToCart(productId) {
      if (this.cartLoading[productId]) return;
      this.cartLoading = { ...this.cartLoading, [productId]: true };
      this.error = null;

      try {
        await axios.post('/api/carts/cart-items/add/', {
          product: productId,
          quantity: 1,
        });
        // Instead of push, always refetch the cart!
        await this.fetchCartItems();
      } catch (error) {
        console.error('Add to cart error:', error);
        this.error = "Failed to add to cart.";
      } finally {
        this.cartLoading = { ...this.cartLoading, [productId]: false };
      }
    },

    async incrementQuantity(productId) {
      const item = this.carts.find((c) => c.product.id === productId);
      if (!item) return;

      if (this.cartLoading[productId]) return;
      this.cartLoading = { ...this.cartLoading, [productId]: true };
      this.error = null;

      try {
        const newQuantity = item.quantity + 1;
        const response = await axios.put(`/api/carts/cart-item/${item.id}/update/`, {
          quantity: newQuantity,
        });
        item.quantity = response.data.quantity || newQuantity;
      } catch (err) {
        console.error("Increment error:", err);
        this.error = "Failed to increment quantity.";
      } finally {
        this.cartLoading = { ...this.cartLoading, [productId]: false };
      }
    },

    async decrementQuantity(productId) {
      const item = this.carts.find((c) => c.product.id === productId);
      if (!item) return;

      if (this.cartLoading[productId]) return;
      this.cartLoading = { ...this.cartLoading, [productId]: true };
      this.error = null;

      try {
        if (item.quantity > 1) {
          await this.updateQuantity(item.id, item.quantity - 1);
        } else {
          await this.deleteItem(item.id);
          // Remove item from carts immediately
          this.carts = this.carts.filter((c) => c.id !== item.id);
        }
      } catch (error) {
        console.error("Decrement error:", error);
        this.error = "Failed to decrement quantity.";
      } finally {
        this.cartLoading = { ...this.cartLoading, [productId]: false };
      }
    },

    async deleteItem(itemId) {
      try {
        await axios.delete(`/api/carts/cart-item/${itemId}/delete/`);
        this.carts = this.carts.filter((item) => item.id !== itemId);
      } catch (err) {
        console.error("Delete error:", err);
        this.error = "Failed to delete item.";
      }
    },

    async updateQuantity(cartId, newQuantity) {
      if (!cartId || newQuantity < 1) return;

      try {
        const res = await axios.put(`/api/carts/cart-item/${cartId}/update/`, {
          quantity: newQuantity,
        });
        const index = this.carts.findIndex((c) => c.id === cartId);
        if (index !== -1) {
          this.carts[index] = {
            ...this.carts[index],
            quantity: res.data.quantity || newQuantity,
          };
        }
      } catch (err) {
        console.error("Update error:", err);
        this.error = "Failed to update quantity.";
      }
    },

    getItemTotal(item) {
      const price = parseFloat(item?.product?.price || 0);
      const qty = parseInt(item?.quantity || 0);
      return (isNaN(price) || isNaN(qty) ? 0 : price * qty).toFixed(2);
    },

    getImage(product) {
      if (
        !product?.images ||
        !Array.isArray(product.images) ||
        product.images.length === 0
      ) {
        return "/placeholder-image.jpg";
      }
      return `https://techrems.pythonanywhere.com${product.images[0].image}`;
    },

    truncate(text, max = 30) {
      return !text ? "" : text.length > max ? text.slice(0, max) + "..." : text;
    },

    goBack() {
      router.back();
    },

    checkout() {
      router.push("/checkout");
    },
  },
});