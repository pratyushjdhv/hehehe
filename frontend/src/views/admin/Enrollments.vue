<template>
  <div class="container mt-4">
    <h2>Enrollments</h2>
    <p class="text-muted">Admin enrollments page - Enroll students in batches</p>
    <div class="alert alert-info">
      This page would allow enrolling students into batches.
      Use userAPI.getAll({ role: 'student' }) and batchAPI.getAll() to populate dropdowns,
      then call enrollmentAPI.create()
    </div>
  </div>
</template>

<script setup>
// Implement using enrollmentAPI, userAPI, and batchAPI
</script>
