// stores/cart.js
import { defineStore } from "pinia";
import axios from "axios";
import { useToast } from "vue-toastification";

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
      const toast = useToast();
      this.isLoading = true;
      this.error = null;
      try {
        const response = await axios.get("/api/carts/customer/cart-items/");
        const cartItems = response.data || [];
        this.carts = cartItems;
        await this.validateAndAdjustCartQuantities(cartItems);
      } catch (err) {
        this.error = "Failed to load cart items.";
        this.carts = [];
        toast.error(this.error);
      } finally {
        this.isLoading = false;
      }
    },

    async validateAndAdjustCartQuantities(cartItems) {
      const toast = useToast();
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
          toast.error(`Stock check failed for product ${item.product.id}`);
          adjustedItems.push(item);
        }
      }

      this.carts = adjustedItems;
      if (hasAdjustments) {
        toast.info("Some items in your cart were adjusted due to stock changes.");
      }
    },

    async checkProductStock(productId) {
      const toast = useToast();
      try {
        const response = await axios.get(`/api/products/${productId}/retrieve/`);
        return response.data.stock || 0;
      } catch (error) {
        toast.error(`Error fetching stock for product ${productId}`);
        return 0;
      }
    },

    async addToCart(productId) {
      const toast = useToast();
      if (this.cartLoading[productId]) return;

      this.cartLoading = { ...this.cartLoading, [productId]: true };
      this.error = null;
      this.clearStockAlert(productId);

      try {
        const stock = await this.checkProductStock(productId);
        if (stock <= 0) {
          this.showStockAlert(productId, "This item is out of stock.");
          toast.error("This item is out of stock.");
          return;
        }

        const existingItem = this.carts.find(c => c.product.id === productId);
        const currentQty = existingItem ? existingItem.quantity : 0;

        if (currentQty >= stock) {
          this.showStockAlert(productId, `Cannot add more. Only ${stock} in stock.`);
          toast.error(`Cannot add more. Only ${stock} in stock.`);
          return;
        }

        await axios.post("/api/carts/cart-items/add/", {
          product: productId,
          quantity: 1,
        });

        await this.fetchCartItems();
        toast.success("Added to cart.");
      } catch (error) {
        this.error = "Failed to add to cart.";
        toast.error(this.error);
      } finally {
        this.cartLoading = { ...this.cartLoading, [productId]: false };
      }
    },

    async incrementQuantity(productId) {
      const toast = useToast();
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
          toast.error(`Cannot add more. Only ${stock} in stock.`);
          return;
        }

        const newQty = item.quantity + 1;
        const response = await axios.put(`/api/carts/cart-item/${item.id}/update/`, {
          quantity: newQty,
        });

        item.quantity = response.data.quantity || newQty;
      } catch (error) {
        this.error = "Failed to increment quantity.";
        toast.error(this.error);
      } finally {
        this.cartLoading = { ...this.cartLoading, [productId]: false };
      }
    },

    async decrementQuantity(productId) {
      const toast = useToast();
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
        this.error = "Failed to decrement quantity.";
        toast.error(this.error);
      } finally {
        this.cartLoading = { ...this.cartLoading, [productId]: false };
      }
    },

    async updateQuantity(itemId, quantity) {
      const toast = useToast();
      try {
        const response = await axios.put(`/api/carts/cart-item/${itemId}/update/`, { quantity });
        const index = this.carts.findIndex(c => c.id === itemId);
        if (index !== -1) {
          this.carts[index].quantity = response.data.quantity || quantity;
        }
      } catch (error) {
        this.error = "Failed to update quantity.";
        toast.error(this.error);
      }
    },

    async deleteItem(itemId) {
      const toast = useToast();
      try {
        await axios.delete(`/api/carts/cart-item/${itemId}/delete/`);
        this.carts = this.carts.filter(c => c.id !== itemId);
        toast.success("Item removed from cart.");
      } catch (error) {
        this.error = "Failed to remove item.";
        toast.error(this.error);
      }
    },

    showStockAdjustmentAlert() {
      const toast = useToast();
      toast.info("Cart items adjusted due to stock changes.");
    },

    clearStockAlert(productId) {
      this.stockAlerts = { ...this.stockAlerts, [productId]: null };
    },
  },
});
