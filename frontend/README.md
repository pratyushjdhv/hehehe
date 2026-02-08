# CoachMaster Frontend

Vue.js 3 frontend application for coaching institute management system.

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Run Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### 3. Build for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── public/
│   └── index.html           # HTML template
├── src/
│   ├── assets/              # Static assets
│   ├── components/          # Reusable components
│   │   └── Navbar.vue
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
│   ├── App.vue              # Root component
│   └── main.js              # Application entry point
├── package.json
└── vite.config.js
```

## Features Implemented

### Authentication
- ✅ Login page with email/password
- ✅ Register page with role selection
- ✅ JWT token management
- ✅ Role-based routing
- ✅ Auto-redirect based on user role

### Admin Pages
- ✅ Dashboard with statistics
- ✅ Courses management (full CRUD)
- ⚠️ Batches, Enrollments, Payments (placeholders - implement following Courses.vue pattern)

### Instructor Pages
- ✅ Dashboard with batch info
- ⚠️ Batches list and Attendance marking (placeholders - implement using respective APIs)

### Student Pages
- ✅ Dashboard with enrollment and fee info
- ⚠️ Attendance history (placeholder - implement using attendanceAPI)

## API Integration

All API calls are centralized in `src/services/api.js`:

- **authAPI** - Authentication endpoints
- **userAPI** - User management
- **courseAPI** - Course management
- **batchAPI** - Batch management
- **enrollmentAPI** - Enrollment management
- **paymentAPI** - Payment management
- **attendanceAPI** - Attendance management
- **dashboardAPI** - Dashboard data

## State Management

Uses Pinia for state management:
- `useAuthStore` - Manages authentication state (user, token, role)

## Routing

Protected routes with role-based access control:
- `/login` - Public
- `/register` - Public
- `/admin/*` - Admin only
- `/instructor/*` - Instructor only
- `/student/*` - Student only

## Development Tips

### Completing Placeholder Pages

Several pages are placeholders with implementation hints. To complete them:

1. **Admin Batches Page**: Follow the same pattern as `Courses.vue`
   - Use `batchAPI` instead of `courseAPI`
   - Include course and instructor selection dropdowns

2. **Admin Enrollments Page**:
   - Fetch students using `userAPI.getAll({ role: 'student' })`
   - Fetch batches using `batchAPI.getAll()`
   - Create enrollment with `enrollmentAPI.create()`

3. **Admin Payments Page**:
   - Similar to Enrollments
   - Use `paymentAPI.create()` with student_id, amount, date

4. **Instructor Attendance Page**:
   - Select batch from `batchAPI.getAll()`
   - Fetch students using `batchAPI.getStudents(batchId)`
   - Mark attendance with `attendanceAPI.mark()`

5. **Student Attendance Page**:
   - Fetch using `attendanceAPI.getByStudent(studentId)`
   - Display in table format

### Adding New Features

1. Create new view component in appropriate directory
2. Add route in `src/router/index.js`
3. Add navigation link in `Navbar.vue` if needed
4. Use existing API methods from `services/api.js`

## Common Issues

### "Module not found"
```bash
npm install
```

### "CORS Error"
Backend should have CORS enabled. Check `backend/app/__init__.py`

### "Cannot read properties of null"
Check if API is running and returning data in expected format

### "Navigation guard error"
Ensure token is valid and stored in localStorage

## Testing

1. Start backend: `cd ../backend && python run.py`
2. Start frontend: `npm run dev`
3. Register a user (try all three roles)
4. Test login with each role
5. Verify role-based redirects work
6. Test CRUD operations on courses

## Next Steps

1. Complete placeholder pages following the patterns provided
2. Add form validation
3. Add loading states
4. Add error handling and user feedback
5. Add confirmation dialogs for delete actions
6. Style improvements
7. Responsive design enhancements

## Technologies Used

- Vue.js 3 (Composition API)
- Vue Router 4
- Pinia (State Management)
- Axios (HTTP Client)
- Bootstrap 5 (CSS Framework)
- Vite (Build Tool)
