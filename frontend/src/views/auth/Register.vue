<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">Register</h2>
            
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            <div v-if="success" class="alert alert-success">{{ success }}</div>
            
            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input 
                  v-model="form.full_name" 
                  type="text" 
                  class="form-control" 
                  required
                >
              </div>
              
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input 
                  v-model="form.email" 
                  type="email" 
                  class="form-control" 
                  required
                >
              </div>
              
              <div class="mb-3">
                <label class="form-label">Password</label>
                <input 
                  v-model="form.password" 
                  type="password" 
                  class="form-control" 
                  required
                  minlength="6"
                >
              </div>
              
              <div class="mb-3">
                <label class="form-label">Role</label>
                <select v-model="form.role" class="form-select" required>
                  <option value="">Select role</option>
                  <option value="admin">Admin</option>
                  <option value="instructor">Instructor</option>
                  <option value="student">Student</option>
                </select>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Phone (optional)</label>
                <input 
                  v-model="form.phone" 
                  type="tel" 
                  class="form-control"
                >
              </div>
              
              <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                {{ loading ? 'Registering...' : 'Register' }}
              </button>
            </form>
            
            <p class="text-center mt-3">
              Already have an account? <router-link to="/login">Login</router-link>
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
import { authAPI } from '@/services/api'

const router = useRouter()

const form = ref({
  email: '',
  password: '',
  full_name: '',
  role: '',
  phone: ''
})

const error = ref('')
const success = ref('')
const loading = ref(false)

const handleRegister = async () => {
  try {
    loading.value = true
    error.value = ''
    success.value = ''
    
    await authAPI.register(form.value)
    
    success.value = 'Registration successful! Redirecting to login...'
    
    setTimeout(() => {
      router.push('/login')
    }, 2000)
    
  } catch (err) {
    error.value = err.response?.data?.message || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>
