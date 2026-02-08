<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Courses</h2>
      <button class="btn btn-primary" @click="openCreateModal">
        Create Course
      </button>
    </div>
    
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Fee</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="course in courses" :key="course.id">
            <td>{{ course.id }}</td>
            <td>{{ course.name }}</td>
            <td>{{ course.description }}</td>
            <td>₹{{ course.total_fee }}</td>
            <td>
              <button class="btn btn-sm btn-info" @click="editCourse(course)">
                Edit
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="modal d-block" tabindex="-1" style="background: rgba(0,0,0,0.5)">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingCourse ? 'Edit' : 'Create' }} Course</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveCourse">
              <div class="mb-3">
                <label class="form-label">Name</label>
                <input v-model="courseForm.name" type="text" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="courseForm.description" class="form-control"></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Total Fee</label>
                <input v-model="courseForm.total_fee" type="number" step="0.01" class="form-control" required>
              </div>
              <button type="submit" class="btn btn-primary">Save</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { courseAPI } from '@/services/api'

const courses = ref([])
const showModal = ref(false)
const editingCourse = ref(null)
const courseForm = ref({ name: '', description: '', total_fee: 0 })

const loadCourses = async () => {
  const response = await courseAPI.getAll()
  courses.value = response.data.courses
}

const openCreateModal = () => {
  editingCourse.value = null
  courseForm.value = { name: '', description: '', total_fee: 0 }
  showModal.value = true
}

const editCourse = (course) => {
  editingCourse.value = course
  courseForm.value = { ...course }
  showModal.value = true
}

const saveCourse = async () => {
  try {
    if (editingCourse.value) {
      await courseAPI.update(editingCourse.value.id, courseForm.value)
    } else {
      await courseAPI.create(courseForm.value)
    }
    closeModal()
    loadCourses()
  } catch (error) {
    console.error('Failed to save course:', error)
    alert('Failed to save course')
  }
}

const closeModal = () => {
  showModal.value = false
  editingCourse.value = null
  courseForm.value = { name: '', description: '', total_fee: 0 }
}

onMounted(loadCourses)
</script>
