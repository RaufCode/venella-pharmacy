// stores/cart.js
import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";
import { useNotificationStore } from "./notification";

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
        const cartItems = response.data || [];
        
        // Set the carts immediately with the fetched data
        this.carts = cartItems;
        
        // Validate and adjust quantities in the background (non-blocking)
        // This prevents the cart from appearing empty while validation happens
        this.validateAndAdjustCartQuantities(cartItems).catch(error => {
          console.error("Validation error (non-critical):", error);
        });
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
              const adjustedItem = { ...item, quantity: currentStock };
              adjustedItems.push(adjustedItem);
              await this.updateQuantity(item.id, currentStock);
              hasAdjustments = true;
            } else {
              await this.deleteItem(item.id);
              hasAdjustments = true;
              continue;
            }
          } else {
            adjustedItems.push(item);
          }
        } catch (error) {
          console.error(`Error checking stock for product ${item.product.id}:`, error);
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

      const notificationStore = useNotificationStore();
      this.cartLoading = { ...this.cartLoading, [productId]: true };
      this.error = null;
      this.clearStockAlert(productId);

      try {
        const availableStock = await this.checkProductStock(productId);

        if (availableStock <= 0) {
          this.showStockAlert(productId, "This item is out of stock.");
          return;
        }

        const existingItem = this.carts.find(c => c.product.id === productId);
        const currentCartQuantity = existingItem ? existingItem.quantity : 0;

        if (currentCartQuantity >= availableStock) {
          this.showStockAlert(productId, `Cannot add more. Only ${availableStock} items available in stock.`);
          return;
        }

        await axios.post('/api/carts/cart-items/add/', {
          product: productId,
          quantity: 1,
        });

        await this.fetchCartItems();

        const addedProduct = this.carts.find(c => c.product.id === productId)?.product;
        if (addedProduct) {
          notificationStore.addNotification({
            id: Date.now(),
            type: "CART_ADD",
            message: `${addedProduct.name} added to cart.`,
            read: false,
            created_at: new Date().toISOString(),
          });
        }
      } catch (error) {
        console.error('Add to cart error:', error);
        this.error = "Failed to add to cart.";
      } finally {
        this.cartLoading = { ...this.cartLoading, [productId]: false };
      }
    },

    async incrementQuantity(productId) {
      if (this.cartLoading[productId]) return;

      const item = this.carts.find((c) => c.product.id === productId);
      if (!item) return;

      this.cartLoading = { ...this.cartLoading, [productId]: true };
      this.error = null;
      this.clearStockAlert(productId);

      try {
        const availableStock = await this.checkProductStock(productId);
        if (item.quantity >= availableStock) {
          this.showStockAlert(productId, `Cannot add more. Only ${availableStock} items available in stock.`);
          return;
        }

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
      if (this.cartLoading[productId]) return;

      const item = this.carts.find((c) => c.product.id === productId);
      if (!item) return;

      const notificationStore = useNotificationStore();
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
        const response = await axios.put(`/api/carts/cart-item/${itemId}/update/`, {
          quantity,
        });

        const index = this.carts.findIndex((c) => c.id === itemId);
        if (index !== -1) {
          this.carts[index].quantity = response.data.quantity || quantity;
        }
      } catch (err) {
        console.error("Update error:", err);
        this.error = "Failed to update quantity.";
      }
    },

    async deleteItem(itemId) {
      const item = this.carts.find(c => c.id === itemId);
      const notificationStore = useNotificationStore();

      try {
        await axios.delete(`/api/carts/cart-item/${itemId}/delete/`);
        this.carts = this.carts.filter((c) => c.id !== itemId);

        if (item) {
          notificationStore.addNotification({
            id: Date.now(),
            type: "CART_REMOVE",
            message: `${item.product.name} removed from cart.`,
            read: false,
            created_at: new Date().toISOString(),
          });
        }
      } catch (error) {
        console.error("Delete error:", error);
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
