import { defineStore } from 'pinia'
import { getUser, setUser, removeUser, getToken, setToken, removeToken } from '@/utils/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: getUser(),
    token: getToken(),
    isAuthenticated: !!getToken()
  }),
  
  getters: {
    userRole: (state) => state.user?.role,
    isAdmin: (state) => state.user?.role === 'admin',
    isInstructor: (state) => state.user?.role === 'instructor',
    isStudent: (state) => state.user?.role === 'student'
  },
  
  actions: {
    setAuth(token, user) {
      this.token = token
      this.user = user
      this.isAuthenticated = true
      setToken(token)
      setUser(user)
    },
    
    clearAuth() {
      this.token = null
      this.user = null
      this.isAuthenticated = false
      removeToken()
      removeUser()
    }
  }
})
