// stores/cart.js
import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";

export const useCartStore = defineStore("cart", {
  state: () => ({
    carts: [],
    isLoading: false,
    error: null,
    cartLoading: {},
    stockAlerts: {},
  }),

  getters: {
    cartCount: (state) => state.carts.length,
    subtotal: (state) =>
      state.carts
        .reduce((total, item) => {
          const price = parseFloat(item?.product?.price || 0);
          const qty = parseInt(item?.quantity || 0);
          return total + (isNaN(price) || isNaN(qty) ? 0 : price * qty);
        }, 0)
        .toFixed(2),
  },

  actions: {
    async fetchCartItems() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await axios.get("/api/carts/customer/cart-items/");
        const cartItems = response.data || [];
        this.carts = cartItems;
        await this.validateAndAdjustCartQuantities(cartItems);
      } catch (err) {
        console.error("Fetch error:", err);
        this.error = "Failed to load cart items.";
        this.carts = [];
      } finally {
        this.isLoading = false;
      }
    },

    async validateAndAdjustCartQuantities(cartItems) {
      const adjustedItems = [];
      let hasAdjustments = false;

      for (const item of cartItems) {
        try {
          const stockResponse = await axios.get(`/api/products/${item.product.id}/retrieve/`);
          const currentStock = stockResponse.data.stock || 0;

          if (item.quantity > currentStock) {
            if (currentStock > 0) {
              await this.updateQuantity(item.id, currentStock);
              adjustedItems.push({ ...item, quantity: currentStock });
              hasAdjustments = true;
            } else {
              await this.deleteItem(item.id);
              hasAdjustments = true;
            }
          } else {
            adjustedItems.push(item);
          }
        } catch (error) {
          console.error(`Stock check failed for product ${item.product.id}:`, error);
          adjustedItems.push(item);
        }
      }

      this.carts = adjustedItems;
      if (hasAdjustments) {
        this.showStockAdjustmentAlert();
      }
    },

    async checkProductStock(productId) {
      try {
        const response = await axios.get(`/api/products/${productId}/retrieve/`);
        return response.data.stock || 0;
      } catch (error) {
        console.error(`Error fetching stock for product ${productId}:`, error);
        return 0;
      }
    },

    async addToCart(productId) {
      if (this.cartLoading[productId]) return;

      this.cartLoading = { ...this.cartLoading, [productId]: true };
      this.error = null;
      this.clearStockAlert(productId);

      try {
        const stock = await this.checkProductStock(productId);
        if (stock <= 0) {
          this.showStockAlert(productId, "This item is out of stock.");
          return;
        }

        const existingItem = this.carts.find(c => c.product.id === productId);
        const currentQty = existingItem ? existingItem.quantity : 0;

        if (currentQty >= stock) {
          this.showStockAlert(productId, `Cannot add more. Only ${stock} in stock.`);
          return;
        }

        await axios.post("/api/carts/cart-items/add/", {
          product: productId,
          quantity: 1,
        });

        await this.fetchCartItems();
      } catch (error) {
        console.error("Add to cart error:", error);
        this.error = "Failed to add to cart.";
      } finally {
        this.cartLoading = { ...this.cartLoading, [productId]: false };
      }
    },

    async incrementQuantity(productId) {
      if (this.cartLoading[productId]) return;

      const item = this.carts.find(c => c.product.id === productId);
      if (!item) return;

      this.cartLoading = { ...this.cartLoading, [productId]: true };
      this.error = null;
      this.clearStockAlert(productId);

      try {
        const stock = await this.checkProductStock(productId);
        if (item.quantity >= stock) {
          this.showStockAlert(productId, `Cannot add more. Only ${stock} in stock.`);
          return;
        }

        const newQty = item.quantity + 1;
        const response = await axios.put(`/api/carts/cart-item/${item.id}/update/`, {
          quantity: newQty,
        });

        item.quantity = response.data.quantity || newQty;
      } catch (error) {
        console.error("Increment error:", error);
        this.error = "Failed to increment quantity.";
      } finally {
        this.cartLoading = { ...this.cartLoading, [productId]: false };
      }
    },

    async decrementQuantity(productId) {
      if (this.cartLoading[productId]) return;

      const item = this.carts.find(c => c.product.id === productId);
      if (!item) return;

      this.cartLoading = { ...this.cartLoading, [productId]: true };
      this.error = null;
      this.clearStockAlert(productId);

      try {
        if (item.quantity > 1) {
          await this.updateQuantity(item.id, item.quantity - 1);
        } else {
          await this.deleteItem(item.id);
        }
      } catch (error) {
        console.error("Decrement error:", error);
        this.error = "Failed to decrement quantity.";
      } finally {
        this.cartLoading = { ...this.cartLoading, [productId]: false };
      }
    },

    async updateQuantity(itemId, quantity) {
      try {
        const response = await axios.put(`/api/carts/cart-item/${itemId}/update/`, { quantity });
        const index = this.carts.findIndex(c => c.id === itemId);
        if (index !== -1) {
          this.carts[index].quantity = response.data.quantity || quantity;
        }
      } catch (error) {
        console.error("Update quantity error:", error);
        this.error = "Failed to update quantity.";
      }
    },

    async deleteItem(itemId) {
      try {
        await axios.delete(`/api/carts/cart-item/${itemId}/delete/`);
        this.carts = this.carts.filter(c => c.id !== itemId);
      } catch (error) {
        console.error("Delete item error:", error);
        this.error = "Failed to remove item.";
      }
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

    showStockAlert(productId, message) {
      this.stockAlerts[productId] = message;
    },

    clearStockAlert(productId) {
      delete this.stockAlerts[productId];
    },

    showStockAdjustmentAlert() {
      alert("Some items in your cart were adjusted due to stock changes.");
    },
  },
});
