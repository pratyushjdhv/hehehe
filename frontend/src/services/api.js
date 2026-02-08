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
