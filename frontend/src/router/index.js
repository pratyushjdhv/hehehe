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
