<template>
  <div class="container mt-4">
    <h2>Student Dashboard</h2>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>
    
    <div v-else-if="dashboardData.enrolled_batch">
      <div class="card mt-4">
        <div class="card-body">
          <h5 class="card-title">My Enrollment</h5>
          <p><strong>Batch:</strong> {{ dashboardData.enrolled_batch.batch_name }}</p>
          <p><strong>Course:</strong> {{ dashboardData.enrolled_batch.course_name }}</p>
          <p><strong>Instructor:</strong> {{ dashboardData.enrolled_batch.instructor_name }}</p>
          <p><strong>Schedule:</strong> {{ dashboardData.enrolled_batch.schedule_time }}</p>
        </div>
      </div>
      
      <div class="row mt-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Attendance</h5>
              <p><strong>Total Classes:</strong> {{ dashboardData.attendance_summary.total_classes }}</p>
              <p><strong>Present:</strong> {{ dashboardData.attendance_summary.present_count }}</p>
              <p><strong>Percentage:</strong> {{ dashboardData.attendance_summary.attendance_percentage }}%</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Fee Status</h5>
              <p><strong>Total Fee:</strong> ₹{{ dashboardData.fee_status.total_fee }}</p>
              <p><strong>Paid:</strong> ₹{{ dashboardData.fee_status.paid }}</p>
              <p><strong>Balance:</strong> ₹{{ dashboardData.fee_status.balance }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else>
      <div class="alert alert-warning">
        You are not enrolled in any batch yet.
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
    const response = await dashboardAPI.getStudent()
    dashboardData.value = response.data
  } catch (error) {
    console.error('Failed to load dashboard:', error)
  } finally {
    loading.value = false
  }
})
</script>
