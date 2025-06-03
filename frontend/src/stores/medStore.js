import { defineStore } from 'pinia'
import axios from 'axios'

export const useMedStore = defineStore('medStore', {
  state: () => ({
    products: [],
    categories: [],
    showModal: false,
    isSubmitting: false,
    editingProductId: null,
    searchResults: [],
    form: {
      name: '',
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
      try {
        const res = await axios.get('/api/products/categories/')
        this.categories = res.data
      } catch (error) {
        console.error('Error fetching categories:', error)
      }
    },

    async fetchProducts() {
      try {
        const res = await axios.get('/api/products/')
        // Only include products with stock greater than 0
        this.products = res.data.filter(product => product.stock > 0)
      } catch (error) {
        console.error('Error fetching products:', error)
      }
    },

    async searchProducts(query) {
      if (!query.trim()) {
        this.searchResults = []
        return
      }

      try {
        const res = await axios.get(`/api/products/search/?query=${encodeURIComponent(query)}`)
        // Only include search results with stock greater than 0
        this.searchResults = res.data.filter(product => product.stock > 0)
      } catch (error) {
        console.error('Error searching products:', error)
        this.searchResults = []
      }
    },

    async submitForm() {
      if (this.isSubmitting) return
      this.isSubmitting = true

      try {
        const formData = new FormData()
        formData.append('name', this.form.name)
        formData.append('stock', this.form.stock)
        formData.append('price', this.form.price)
        formData.append('category', this.form.category)
        formData.append('description', this.form.description)

        this.form.product_images.forEach(file => {
          formData.append('product_images', file)
        })

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

          alert('Medication updated successfully!')
        } else {
          const response = await axios.post('/api/products/add/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })

          const newProduct = response.data
          if (newProduct.stock > 0) {
            this.products.unshift(newProduct)
          }

          alert('Medication added successfully!')
        }

        this.resetForm()
        this.showModal = false
      } catch (error) {
        console.error('Error submitting form:', error.response?.data || error)
        alert(
          error.response?.data?.detail ||
          'An error occurred while submitting the form.'
        )
      } finally {
        this.isSubmitting = false
      }
    },

    async editProduct(id) {
      try {
        const res = await axios.get(`/api/products/${id}/retrieve/`)
        const product = res.data

        this.form.name = product.name
        this.form.stock = product.stock
        this.form.price = product.price
        this.form.category = product.category.id
        this.form.description = product.description
        this.form.product_images = []

        this.editingProductId = id
        this.showModal = true
      } catch (error) {
        console.error('Error loading product data:', error.response?.data || error)
        alert('Failed to load product details for editing.')
      }
    },

    async deleteProduct(id) {
      if (!confirm('Are you sure you want to delete this product?')) return

      try {
        await axios.delete(`/api/products/${id}/delete/`)
        this.products = this.products.filter(p => p.id !== id)
        alert('Product deleted successfully.')
      } catch (error) {
        console.error('Error deleting product:', error.response?.data || error)
        alert(
          error.response?.data?.detail || 'An error occurred while deleting the product.'
        )
      }
    }
  }
})
