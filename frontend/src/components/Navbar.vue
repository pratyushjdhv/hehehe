<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">CoachMaster</router-link>
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <!-- Admin Navigation -->
          <template v-if="authStore.isAdmin">
            <li class="nav-item">
              <router-link to="/admin/dashboard" class="nav-link">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin/courses" class="nav-link">Courses</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin/batches" class="nav-link">Batches</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin/enrollments" class="nav-link">Enrollments</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin/payments" class="nav-link">Payments</router-link>
            </li>
          </template>
          
          <!-- Instructor Navigation -->
          <template v-if="authStore.isInstructor">
            <li class="nav-item">
              <router-link to="/instructor/dashboard" class="nav-link">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/instructor/batches" class="nav-link">My Batches</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/instructor/attendance" class="nav-link">Attendance</router-link>
            </li>
          </template>
          
          <!-- Student Navigation -->
          <template v-if="authStore.isStudent">
            <li class="nav-item">
              <router-link to="/student/dashboard" class="nav-link">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/student/attendance" class="nav-link">My Attendance</router-link>
            </li>
          </template>
        </ul>
        
        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
              {{ authStore.user?.full_name || 'User' }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><span class="dropdown-item-text"><small>{{ authStore.user?.email }}</small></span></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="#" @click.prevent="handleLogout">Logout</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store'
import { authAPI } from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = async () => {
  try {
    await authAPI.logout()
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    authStore.clearAuth()
    router.push('/login')
  }
}
</script>
