import { defineStore } from 'pinia'
import axios from 'axios'
import { useToast } from "vue-toastification";

export const useMedStore = defineStore('medStore', {
  state: () => ({
    products: [],
    categories: [],
    showModal: false,
    isSubmitting: false,
    editingProductId: null,
    searchResults: [],
    isLoading: false,
    form: {
      name: '',
      brand: '',
      stock: null,
      price: null,
      category: '',
      description: '',
      product_images: []
    }
  }),

  getters: {
    hasProducts(state) {
      return state.products.length > 0
    },
    isEditing(state) {
      return !!state.editingProductId
    }
  },

  actions: {
    resetForm() {
      this.form = {
        name: '',
        brand: '',
        stock: null,
        price: null,
        category: '',
        description: '',
        product_images: []
      }
      this.editingProductId = null
    },

    handleImageUpload(event) {
      this.form.product_images = Array.from(event.target.files)
    },

    async fetchCategories() {
      const toast = useToast();
      try {
        const res = await axios.get('/api/products/categories/')
        this.categories = res.data
      } catch (error) {
        toast.error('Error fetching categories.');
      }
    },

    async fetchProducts() {
      const toast = useToast();
      this.isLoading = true;
      try {
        const res = await axios.get('/api/products/')
        this.products = res.data.filter(product => product.stock > 0)
      } catch (error) {
        toast.error('Error fetching products.');
      } finally {
        this.isLoading = false;
      }
    },

    async searchProducts(query) {
      const toast = useToast();
      this.isLoading = true;
      if (!query.trim()) {
        this.searchResults = []
        this.isLoading = false;
        return
      }
      try {
        const res = await axios.get(`/api/products/search/?query=${encodeURIComponent(query)}`)
        this.searchResults = res.data.filter(product => product.stock > 0)
      } catch (error) {
        toast.error('Error searching products.');
        this.searchResults = [];
      } finally {
        this.isLoading = false;
      }
    },

    async addProduct(formData) {
      const toast = useToast();
      if (this.isSubmitting) return
      this.isSubmitting = true
      try {
        if (this.editingProductId) {
          const response = await axios.put(
            `/api/products/${this.editingProductId}/update/`,
            formData,
            { headers: { 'Content-Type': 'multipart/form-data' } }
          )
          const updatedProduct = response.data
          const index = this.products.findIndex(p => p.id === updatedProduct.id)
          if (index !== -1) {
            if (updatedProduct.stock > 0) {
              this.products[index] = updatedProduct
            } else {
              this.products.splice(index, 1)
            }
          }
          toast.success('Medication updated successfully!')
        } else {
          const response = await axios.post('/api/products/add/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          const newProduct = response.data
          if (newProduct.stock > 0) {
            this.products.unshift(newProduct)
          }
          toast.success('Medication added successfully!')
        }
        this.resetForm()
        this.showModal = false
        await this.fetchProducts()
      } catch (error) {
        toast.error(error.response?.data?.detail || 'An error occurred while submitting the form.')
      } finally {
        this.isSubmitting = false
      }
    },

    // Separate method for updating products (for compatibility with modal)
    async updateProduct(id, formData) {
      this.editingProductId = id
      return this.addProduct(formData)
    },

    // Submit form method for compatibility with existing components
    async submitForm() {
      const formData = new FormData()
      formData.append('name', this.form.name)
      formData.append('brand', this.form.brand)
      formData.append('stock', this.form.stock)
      formData.append('price', this.form.price)
      formData.append('category', this.form.category)
      formData.append('description', this.form.description)

      this.form.product_images.forEach(file => {
        formData.append('product_images', file)
      })

      return this.addProduct(formData)
    },

    async editProduct(id) {
      const toast = useToast();
      try {
        const res = await axios.get(`/api/products/${id}/retrieve/`)
        const product = res.data
        this.form.name = product.name
        this.form.brand = product.brand || ''
        this.form.stock = product.stock
        this.form.price = product.price
        this.form.category = product.category.id
        this.form.description = product.description
        this.form.product_images = []
        this.editingProductId = id
        this.showModal = true
      } catch (error) {
        toast.error('Failed to load product details for editing.')
      }
    },

    async deleteProduct(id) {
      const toast = useToast();
      if (!confirm('Are you sure you want to delete this product?')) return
      try {
        await axios.delete(`/api/products/${id}/delete/`)
        this.products = this.products.filter(p => p.id !== id)
        toast.success('Product deleted successfully.')
      } catch (error) {
        toast.error(error.response?.data?.detail || 'An error occurred while deleting the product.')
      }
    }
  }
})
