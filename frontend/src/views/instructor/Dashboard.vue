<template>
  <div class="container mt-4">
    <h2>Instructor Dashboard</h2>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>
    
    <div v-else>
      <div class="row mt-4">
        <div class="col-md-6 mb-3">
          <div class="card text-center">
            <div class="card-body">
              <h3>{{ dashboardData.total_batches }}</h3>
              <p class="text-muted">My Batches</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-6 mb-3">
          <div class="card text-center">
            <div class="card-body">
              <h3>{{ dashboardData.total_students }}</h3>
              <p class="text-muted">Total Students</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card mt-4">
        <div class="card-body">
          <h5 class="card-title">My Batches</h5>
          <table class="table">
            <thead>
              <tr>
                <th>Batch Name</th>
                <th>Course</th>
                <th>Students</th>
                <th>Schedule</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="batch in dashboardData.my_batches" :key="batch.batch_id">
                <td>{{ batch.batch_name }}</td>
                <td>{{ batch.course_name }}</td>
                <td>{{ batch.student_count }}</td>
                <td>{{ batch.schedule_time }}</td>
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

onMounted(async () => {
  try {
    const response = await dashboardAPI.getInstructor()
    dashboardData.value = response.data
  } catch (error) {
    console.error('Failed to load dashboard:', error)
  } finally {
    loading.value = false
  }
})
</script>
