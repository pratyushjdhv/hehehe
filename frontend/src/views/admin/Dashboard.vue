<template>
  <div class="container mt-4">
    <h2>Admin Dashboard</h2>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>
    
    <div v-else>
      <div class="row mt-4">
        <div class="col-md-3 mb-3">
          <div class="card text-center">
            <div class="card-body">
              <h3>{{ dashboardData.total_students }}</h3>
              <p class="text-muted">Total Students</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-3 mb-3">
          <div class="card text-center">
            <div class="card-body">
              <h3>{{ dashboardData.total_instructors }}</h3>
              <p class="text-muted">Total Instructors</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-3 mb-3">
          <div class="card text-center">
            <div class="card-body">
              <h3>{{ dashboardData.total_courses }}</h3>
              <p class="text-muted">Total Courses</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-3 mb-3">
          <div class="card text-center">
            <div class="card-body">
              <h3>₹{{ dashboardData.total_revenue }}</h3>
              <p class="text-muted">Total Revenue</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card mt-4">
        <div class="card-body">
          <h5 class="card-title">Recent Enrollments</h5>
          <table class="table">
            <thead>
              <tr>
                <th>Student</th>
                <th>Batch</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="enrollment in dashboardData.recent_enrollments" :key="enrollment.student_name">
                <td>{{ enrollment.student_name }}</td>
                <td>{{ enrollment.batch_name }}</td>
                <td>{{ formatDate(enrollment.enrollment_date) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { dashboardAPI } from '@/services/api'

const dashboardData = ref({})
const loading = ref(true)

const formatDate = (date) => new Date(date).toLocaleDateString()

onMounted(async () => {
  try {
    const response = await dashboardAPI.getAdmin()
    dashboardData.value = response.data
  } catch (error) {
    console.error('Failed to load dashboard:', error)
  } finally {
    loading.value = false
  }
})
</script>
