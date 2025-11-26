import { defineStore } from 'pinia'
import axios from '../api/axios'
import router from '../router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    role: localStorage.getItem('role') || null,
    username: localStorage.getItem('username') || null
  }),
  actions: {
    async login(username, password) {
      const res = await axios.post('/auth/login', { username, password })
      this.token = res.data.access_token
      this.role = res.data.role
      this.username = username
      localStorage.setItem('token', this.token)
      localStorage.setItem('role', this.role)
      localStorage.setItem('username', this.username)
      return this.role
    },
    logout() {
      this.token = null
      this.role = null
      this.username = null
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      localStorage.removeItem('username')
      router.push('/login')
    }
  }
})
