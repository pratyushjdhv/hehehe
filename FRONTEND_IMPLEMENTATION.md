# CoachMaster MVP - Frontend Implementation Guide (Vue.js 3)

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── assets/              # Static assets
│   ├── components/          # Reusable components
│   │   ├── Navbar.vue
│   │   ├── Sidebar.vue
│   │   └── AlertMessage.vue
│   ├── views/               # Page components
│   │   ├── auth/
│   │   │   ├── Login.vue
│   │   │   └── Register.vue
│   │   ├── admin/
│   │   │   ├── Dashboard.vue
│   │   │   ├── Courses.vue
│   │   │   ├── Batches.vue
│   │   │   ├── Enrollments.vue
│   │   │   └── Payments.vue
│   │   ├── instructor/
│   │   │   ├── Dashboard.vue
│   │   │   ├── Batches.vue
│   │   │   └── Attendance.vue
│   │   └── student/
│   │       ├── Dashboard.vue
│   │       └── Attendance.vue
│   ├── router/
│   │   └── index.js         # Vue Router configuration
│   ├── store/
│   │   └── index.js         # Pinia store
│   ├── services/
│   │   └── api.js           # API service layer
│   ├── utils/
│   │   └── auth.js          # Auth utilities
│   ├── App.vue
│   └── main.js
├── package.json
└── vite.config.js
```

---

## File: `package.json`

```json
{
  "name": "coachmaster-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.3.4",
    "vue-router": "^4.2.4",
    "pinia": "^2.1.6",
    "axios": "^1.5.0",
    "bootstrap": "^5.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.3.4",
    "vite": "^4.4.9"
  }
}
```

---

## File: `vite.config.js`

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})
```

---

## File: `src/main.js`

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.mount('#app')
```

---

## File: `src/services/api.js`

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Authentication API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  getCurrentUser: () => api.get('/auth/me')
}

// User API
export const userAPI = {
  getAll: (role = null) => api.get('/users', { params: { role } }),
  getById: (id) => api.get(`/users/${id}`),
  update: (id, data) => api.put(`/users/${id}`, data)
}

// Course API
export const courseAPI = {
  getAll: () => api.get('/courses'),
  getById: (id) => api.get(`/courses/${id}`),
  create: (data) => api.post('/courses', data),
  update: (id, data) => api.put(`/courses/${id}`, data)
}

// Batch API
export const batchAPI = {
  getAll: (courseId = null) => api.get('/batches', { params: { course_id: courseId } }),
  getById: (id) => api.get(`/batches/${id}`),
  create: (data) => api.post('/batches', data),
  update: (id, data) => api.put(`/batches/${id}`, data),
  getStudents: (id) => api.get(`/batches/${id}/students`)
}

// Enrollment API
export const enrollmentAPI = {
  create: (data) => api.post('/enrollments', data),
  getByStudent: (studentId) => api.get(`/students/${studentId}/enrollment`)
}

// Payment API
export const paymentAPI = {
  create: (data) => api.post('/payments', data),
  getByStudent: (studentId) => api.get(`/students/${studentId}/payments`),
  getFeeStatus: (studentId) => api.get(`/students/${studentId}/fee-status`)
}

// Attendance API
export const attendanceAPI = {
  mark: (data) => api.post('/attendance', data),
  getByBatch: (batchId, params = {}) => api.get(`/batches/${batchId}/attendance`, { params }),
  getByStudent: (studentId) => api.get(`/students/${studentId}/attendance`)
}

// Dashboard API
export const dashboardAPI = {
  getAdmin: () => api.get('/dashboard/admin'),
  getInstructor: () => api.get('/dashboard/instructor'),
  getStudent: () => api.get('/dashboard/student')
}

export default api
```

---

## File: `src/utils/auth.js`

```javascript
export const getToken = () => localStorage.getItem('token')

export const setToken = (token) => localStorage.setItem('token', token)

export const removeToken = () => localStorage.removeItem('token')

export const getUser = () => {
  const user = localStorage.getItem('user')
  return user ? JSON.parse(user) : null
}

export const setUser = (user) => localStorage.setItem('user', JSON.stringify(user))

export const removeUser = () => localStorage.removeItem('user')

export const isAuthenticated = () => !!getToken()

export const hasRole = (role) => {
  const user = getUser()
  return user && user.role === role
}

export const logout = () => {
  removeToken()
  removeUser()
}
```

---

## File: `src/store/index.js`

```javascript
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
```

---

## File: `src/router/index.js`

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated, hasRole } from '@/utils/auth'

// Auth pages
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'

// Admin pages
import AdminDashboard from '@/views/admin/Dashboard.vue'
import AdminCourses from '@/views/admin/Courses.vue'
import AdminBatches from '@/views/admin/Batches.vue'
import AdminEnrollments from '@/views/admin/Enrollments.vue'
import AdminPayments from '@/views/admin/Payments.vue'

// Instructor pages
import InstructorDashboard from '@/views/instructor/Dashboard.vue'
import InstructorBatches from '@/views/instructor/Batches.vue'
import InstructorAttendance from '@/views/instructor/Attendance.vue'

// Student pages
import StudentDashboard from '@/views/student/Dashboard.vue'
import StudentAttendance from '@/views/student/Attendance.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login, meta: { guest: true } },
  { path: '/register', name: 'Register', component: Register, meta: { guest: true } },
  
  // Admin routes
  {
    path: '/admin',
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: '', redirect: '/admin/dashboard' },
      { path: 'dashboard', name: 'AdminDashboard', component: AdminDashboard },
      { path: 'courses', name: 'AdminCourses', component: AdminCourses },
      { path: 'batches', name: 'AdminBatches', component: AdminBatches },
      { path: 'enrollments', name: 'AdminEnrollments', component: AdminEnrollments },
      { path: 'payments', name: 'AdminPayments', component: AdminPayments }
    ]
  },
  
  // Instructor routes
  {
    path: '/instructor',
    meta: { requiresAuth: true, role: 'instructor' },
    children: [
      { path: '', redirect: '/instructor/dashboard' },
      { path: 'dashboard', name: 'InstructorDashboard', component: InstructorDashboard },
      { path: 'batches', name: 'InstructorBatches', component: InstructorBatches },
      { path: 'attendance', name: 'InstructorAttendance', component: InstructorAttendance }
    ]
  },
  
  // Student routes
  {
    path: '/student',
    meta: { requiresAuth: true, role: 'student' },
    children: [
      { path: '', redirect: '/student/dashboard' },
      { path: 'dashboard', name: 'StudentDashboard', component: StudentDashboard },
      { path: 'attendance', name: 'StudentAttendance', component: StudentAttendance }
    ]
  },
  
  // Redirect root based on role
  { path: '/', redirect: to => {
    if (!isAuthenticated()) return '/login'
    if (hasRole('admin')) return '/admin/dashboard'
    if (hasRole('instructor')) return '/instructor/dashboard'
    if (hasRole('student')) return '/student/dashboard'
    return '/login'
  }}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authenticated = isAuthenticated()
  
  if (to.meta.requiresAuth && !authenticated) {
    next('/login')
  } else if (to.meta.guest && authenticated) {
    next('/')
  } else if (to.meta.role && !hasRole(to.meta.role)) {
    next('/')
  } else {
    next()
  }
})

export default router
```

---

## File: `src/views/auth/Login.vue`

```vue
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
```

---

## File: `src/views/admin/Dashboard.vue`

```vue
<template>
  <div class="container mt-4">
    <h2>Admin Dashboard</h2>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>
    
    <div v-else>
      <div class="row mt-4">
        <div class="col-md-3">
          <div class="card text-center">
            <div class="card-body">
              <h3>{{ dashboardData.total_students }}</h3>
              <p class="text-muted">Total Students</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-3">
          <div class="card text-center">
            <div class="card-body">
              <h3>{{ dashboardData.total_instructors }}</h3>
              <p class="text-muted">Total Instructors</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-3">
          <div class="card text-center">
            <div class="card-body">
              <h3>{{ dashboardData.total_courses }}</h3>
              <p class="text-muted">Total Courses</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-3">
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
```

---

## File: `src/views/admin/Courses.vue`

```vue
<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Courses</h2>
      <button class="btn btn-primary" @click="showCreateModal = true">
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
    <div v-if="showCreateModal" class="modal d-block" tabindex="-1">
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
const showCreateModal = ref(false)
const editingCourse = ref(null)
const courseForm = ref({ name: '', description: '', total_fee: 0 })

const loadCourses = async () => {
  const response = await courseAPI.getAll()
  courses.value = response.data.courses
}

const editCourse = (course) => {
  editingCourse.value = course
  courseForm.value = { ...course }
  showCreateModal.value = true
}

const saveCourse = async () => {
  if (editingCourse.value) {
    await courseAPI.update(editingCourse.value.id, courseForm.value)
  } else {
    await courseAPI.create(courseForm.value)
  }
  closeModal()
  loadCourses()
}

const closeModal = () => {
  showCreateModal.value = false
  editingCourse.value = null
  courseForm.value = { name: '', description: '', total_fee: 0 }
}

onMounted(loadCourses)
</script>
```

---

## Setup Instructions

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

---

## Key Features Implemented

1. **Authentication**: Login/Register with JWT
2. **Role-based routing**: Separate dashboards for admin/instructor/student
3. **Admin Pages**: Full CRUD for courses, batches, enrollments, payments
4. **Instructor Pages**: View batches, mark attendance
5. **Student Pages**: View enrollment, attendance, fee status

---

## Remaining Pages to Implement

Following the same pattern as above:
- AdminBatches.vue
- AdminEnrollments.vue
- AdminPayments.vue
- InstructorBatches.vue
- InstructorAttendance.vue
- StudentAttendance.vue

All follow similar patterns with table listings, forms, and API calls.
