# CoachMaster — MVP Version (1 Week - 2 Developers)

## Overview
This is a **drastically reduced scope** focusing on the absolute core features needed to run a coaching institute. This MVP can be completed in 1 week by 2 developers.

---

## Core Features (MVP)

### 1. User Management & Authentication (Priority: CRITICAL)
**What's Included:**
- User registration (Admin, Instructor, Student only - NO parents, front-desk, or other roles)
- Login/Logout with JWT
- Basic profile view/edit
- Role-based access control (3 roles only)

**What's Removed:**
- Parent/Guardian accounts
- Front-desk/Receptionist accounts
- Batch Manager/Coordinator
- External vendors
- Accountant access
- IT Support accounts
- Complex profile management
- Account activation/deactivation workflows

### 2. Course & Batch Management (Priority: CRITICAL)
**What's Included:**
- Create/View/Edit courses (name, description, fee)
- Create/View batches (linked to course, with instructor and simple schedule)
- Basic batch-instructor assignment

**What's Removed:**
- Batch deletion (to prevent data loss)
- Room management
- Complex scheduling with conflict detection
- Batch capacity limits
- Multiple instructors per batch
- Batch coordinator assignments

### 3. Enrollment & Fee Management (Priority: CRITICAL)
**What's Included:**
- Enroll student in a batch (one batch per student)
- Record payment (simple - full payment or partial)
- View fee status for a student

**What's Removed:**
- Fee installment plans
- Multiple batch enrollments per student
- Batch transfers
- Fee reminders
- PDF receipt generation
- Complex fee structures
- Discount management
- Refund processing

### 4. Attendance Management (Priority: HIGH)
**What's Included:**
- Mark attendance for a batch (present/absent only)
- View attendance for a student
- View attendance report for a batch

**What's Removed:**
- Leave requests
- Substitution management
- Attendance percentage calculations
- Attendance alerts
- Late/early departure tracking
- Bulk attendance marking optimizations

### 5. Basic Dashboard (Priority: HIGH)
**What's Included:**
- Admin dashboard: Total students, total revenue, recent enrollments
- Instructor dashboard: Their batches, today's schedule
- Student dashboard: Their batch info, attendance count

**What's Removed:**
- Parent dashboard
- Front-desk dashboard
- Complex analytics
- Graphs and charts
- Financial reports
- Attendance trend reports
- Performance analytics

---

## Features Removed Entirely (Move to Phase 2+)

### ❌ Test Management
- Test creation, assignment, submission, grading
- MCQ auto-grading
- Test results and analytics
- AI-generated questions

### ❌ Study Material Management
- Upload/download study materials
- Material organization by topic

### ❌ Doubts & Communication
- Q&A forum
- Doubt posting and resolution
- AI-powered doubt suggestions

### ❌ Notification System
- In-app notifications
- Email notifications
- SMS notifications

### ❌ Enquiry Management
- Lead tracking
- Follow-up reminders
- Conversion tracking

### ❌ Syllabus Tracker
- Topic completion tracking
- Progress monitoring

### ❌ Advanced Scheduling
- Room conflict detection
- Schedule optimization
- Timetable generation

### ❌ Advanced Reporting
- Financial reports
- Attendance analytics
- Performance reports

### ❌ External Integrations
- OpenAI/Gemini APIs
- SendGrid/Email service
- SMS gateway
- Payment gateway integration

---

## Reduced API List (26 APIs - Down from 74)

### Authentication (4 APIs)
1. `POST /auth/register` - Register new user
2. `POST /auth/login` - Login user
3. `POST /auth/logout` - Logout user
4. `GET /auth/me` - Get current user info

### User Management (3 APIs)
5. `GET /users` - List all users (with role filter)
6. `GET /users/{id}` - Get user details
7. `PUT /users/{id}` - Update user profile

### Course Management (5 APIs)
8. `GET /courses` - List all courses
9. `POST /courses` - Create new course
10. `GET /courses/{id}` - Get course details
11. `PUT /courses/{id}` - Update course

### Batch Management (5 APIs)
12. `GET /batches` - List all batches
13. `POST /batches` - Create new batch
14. `GET /batches/{id}` - Get batch details
15. `PUT /batches/{id}` - Update batch
16. `GET /batches/{id}/students` - Get students in a batch

### Enrollment (2 APIs)
17. `POST /enrollments` - Enroll student in batch
18. `GET /students/{id}/enrollment` - Get student's enrollment info

### Payment (3 APIs)
19. `POST /payments` - Record a payment
20. `GET /students/{id}/payments` - Get student payment history
21. `GET /students/{id}/fee-status` - Get fee balance for student

### Attendance (4 APIs)
22. `POST /attendance` - Mark attendance for a class
23. `GET /batches/{id}/attendance` - Get attendance for a batch (with date filter)
24. `GET /students/{id}/attendance` - Get attendance summary for a student

### Dashboard (3 APIs - SIMPLIFIED)
25. `GET /dashboard/admin` - Admin overview (counts only)
26. `GET /dashboard/instructor` - Instructor overview (their batches only)
27. `GET /dashboard/student` - Student overview (their enrollment only)

**Total: 27 APIs** (reduced by 63% from original 74 APIs)

---

## User Stories - MVP Only

### Admin User Stories
**US-A01:** As an admin, I can create courses with name, description, and total fee.
**US-A02:** As an admin, I can create batches and assign them to instructors.
**US-A03:** As an admin, I can view all students and their enrollment status.
**US-A04:** As an admin, I can see a dashboard with total students and total revenue collected.

### Instructor User Stories
**US-I01:** As an instructor, I can view my assigned batches.
**US-I02:** As an instructor, I can mark attendance for my classes.
**US-I03:** As an instructor, I can view attendance reports for my batches.

### Student User Stories
**US-S01:** As a student, I can register and create an account.
**US-S02:** As a student, I can view my enrolled batch information.
**US-S03:** As a student, I can view my attendance record.
**US-S04:** As a student, I can view my fee payment status.

---

## Technology Stack - Simplified

### Backend
- **Framework:** Flask (Python) - Lightweight REST API
- **Database:** SQLite (for MVP - no need for PostgreSQL setup)
- **Authentication:** JWT with Flask-JWT-Extended
- **ORM:** SQLAlchemy

### Frontend
- **Framework:** Vue.js 3 with Composition API
- **Router:** Vue Router (basic routes only)
- **State:** Pinia (minimal state management)
- **UI:** Plain Bootstrap CSS (no custom component library)

### Testing
- **Backend:** pytest with basic test cases
- **Frontend:** Minimal testing (manual testing for MVP)

### Deployment
- **NOT NEEDED FOR 1 WEEK MVP** - Run locally only
- Focus on working code, not deployment infrastructure

---

## Database Schema - MVP

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role ENUM('admin', 'instructor', 'student') NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Courses Table
```sql
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    total_fee DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Batches Table
```sql
CREATE TABLE batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    instructor_id INTEGER NOT NULL,
    batch_name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    schedule_time VARCHAR(100),  -- Simple text like "Mon-Fri 9AM-11AM"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (instructor_id) REFERENCES users(id)
);
```

### Enrollments Table
```sql
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    batch_id INTEGER NOT NULL,
    enrollment_date DATE NOT NULL,
    status ENUM('active', 'completed', 'dropped') DEFAULT 'active',
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (batch_id) REFERENCES batches(id),
    UNIQUE(student_id)  -- One batch per student in MVP
);
```

### Payments Table
```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_mode ENUM('cash', 'card', 'upi', 'bank_transfer') DEFAULT 'cash',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id)
);
```

### Attendance Table
```sql
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status ENUM('present', 'absent') NOT NULL,
    marked_by INTEGER NOT NULL,  -- instructor_id
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (batch_id) REFERENCES batches(id),
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (marked_by) REFERENCES users(id),
    UNIQUE(batch_id, student_id, date)
);
```

**Total: 6 tables** (down from 20+ tables in full version)

---

## 1-Week Development Timeline (2 Developers)

### Day 1-2: Setup & Backend Core
- **Dev 1:** Project setup (Flask, SQLAlchemy, SQLite), database schema, authentication APIs
- **Dev 2:** User management APIs, course APIs

### Day 3-4: Backend Features & Frontend Setup
- **Dev 1:** Batch APIs, enrollment APIs, payment APIs
- **Dev 2:** Attendance APIs, Vue.js project setup, login/register pages

### Day 5-6: Frontend Development
- **Dev 1:** Admin pages (course/batch creation, dashboard)
- **Dev 2:** Instructor pages (batch view, attendance marking), student pages (dashboard, attendance view)

### Day 7: Testing & Integration
- **Both:** Integration testing, bug fixes, final testing, documentation

---

## What Gets Delivered

✅ **Working Features:**
1. User registration and login for admin/instructor/student
2. Create and manage courses
3. Create and manage batches with instructor assignment
4. Enroll students in batches
5. Record payments
6. Mark and view attendance
7. Basic dashboards for all three user types

✅ **Complete working web application** that can manage basic coaching institute operations

✅ **All code organized and documented**

❌ **Not Included:**
- No tests, materials, notifications, enquiries, advanced scheduling
- No PDF generation, email integration, or external APIs
- No advanced analytics or reports
- No deployment setup

---

## Future Phases (Post-MVP)

### Phase 2 (2-3 weeks)
- Test management (create, assign, take tests)
- Study materials upload/download
- Notifications system
- Parent accounts and dashboard

### Phase 3 (2-3 weeks)
- Doubts/Q&A forum
- Enquiry management
- Advanced scheduling with conflict detection
- Room management

### Phase 4 (3-4 weeks)
- Advanced reporting and analytics
- Email/SMS integration
- Payment gateway integration
- AI features (doubt suggestions, question generation)

---

## Success Metrics for MVP

After 1 week, you should have:
- ✅ 27 working APIs
- ✅ 6 database tables with proper relationships
- ✅ Working authentication system
- ✅ Functional admin, instructor, and student interfaces
- ✅ Ability to run a basic coaching institute (enroll students, track attendance, record payments)

**Complexity Reduced By:**
- 63% fewer APIs (27 vs 74)
- 70% fewer database tables (6 vs 20+)
- 80% fewer features (5 core vs 15+ total)
- 50% fewer user roles (3 vs 6+)

This MVP is **realistic and achievable in 1 week by 2 developers** while still providing real value!
