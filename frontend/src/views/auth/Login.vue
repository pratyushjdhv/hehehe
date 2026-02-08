<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">Login to CoachMaster</h2>
            
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input 
                  v-model="email" 
                  type="email" 
                  class="form-control" 
                  required
                  placeholder="Enter your email"
                >
              </div>
              
              <div class="mb-3">
                <label class="form-label">Password</label>
                <input 
                  v-model="password" 
                  type="password" 
                  class="form-control" 
                  required
                  placeholder="Enter your password"
                >
              </div>
              
              <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                {{ loading ? 'Logging in...' : 'Login' }}
              </button>
            </form>
            
            <p class="text-center mt-3">
              Don't have an account? <router-link to="/register">Register</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store'
import { authAPI } from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const response = await authAPI.login({
      email: email.value,
      password: password.value
    })
    
    authStore.setAuth(response.data.token, response.data.user)
    
    // Redirect based on role
    const role = response.data.user.role
    if (role === 'admin') router.push('/admin/dashboard')
    else if (role === 'instructor') router.push('/instructor/dashboard')
    else router.push('/student/dashboard')
    
  } catch (err) {
    error.value = err.response?.data?.message || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>
