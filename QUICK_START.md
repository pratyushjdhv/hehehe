# 🚀 Quick Start Guide - Build CoachMaster MVP in 1 Week

This guide will help you and your friend build the CoachMaster MVP in 1 week.

---

## 📚 Before You Start - Read These First

1. **[MVP_REDUCED_SCOPE.md](MVP_REDUCED_SCOPE.md)** - Understand what you're building (15 min read)
2. **[REDUCTION_SUMMARY.md](REDUCTION_SUMMARY.md)** - See how we reduced the scope (10 min read)

---

## 🗓️ Day-by-Day Plan

### **Day 1 (Monday): Setup & Backend Foundation**

#### Developer 1 (Backend Focus)
**Morning:**
- [ ] Set up Python virtual environment
- [ ] Install Flask and dependencies (see `BACKEND_IMPLEMENTATION.md`)
- [ ] Create database models (User, Course, Batch)
- [ ] Set up SQLAlchemy and Flask-Migrate

**Afternoon:**
- [ ] Implement authentication routes (register, login, logout, /me)
- [ ] Test authentication with Postman/curl
- [ ] Implement user management routes (list, get, update)

**Evening:**
- [ ] Test all user endpoints
- [ ] Document any issues in shared doc

#### Developer 2 (Full-Stack)
**Morning:**
- [ ] Set up Vue.js project with Vite
- [ ] Install dependencies (Vue Router, Pinia, Axios, Bootstrap)
- [ ] Create project structure (see `FRONTEND_IMPLEMENTATION.md`)
- [ ] Set up API service layer

**Afternoon:**
- [ ] Start course API routes (GET, POST, GET/:id, PUT/:id)
- [ ] Test course endpoints

**Evening:**
- [ ] Create Login.vue page
- [ ] Create Register.vue page
- [ ] Test authentication flow

---

### **Day 2 (Tuesday): Core Backend APIs**

#### Developer 1
**Morning:**
- [ ] Create Enrollment and Payment models
- [ ] Implement enrollment routes (create, get by student)
- [ ] Implement payment routes (create, get by student, fee status)

**Afternoon:**
- [ ] Create Attendance model
- [ ] Implement attendance routes (mark, get by batch, get by student)
- [ ] Write helper functions for attendance calculations

**Evening:**
- [ ] Test all new endpoints
- [ ] Fix any bugs
- [ ] Help Developer 2 with integration

#### Developer 2
**Morning:**
- [ ] Complete batch API routes (GET, POST, GET/:id, PUT/:id, GET/:id/students)
- [ ] Test all batch endpoints

**Afternoon:**
- [ ] Create AdminCourses.vue page (list courses, create/edit modal)
- [ ] Create AdminBatches.vue page (list batches, create/edit modal)

**Evening:**
- [ ] Test admin pages with real API
- [ ] Fix any integration issues

---

### **Day 3 (Wednesday): Integration & Admin Pages**

#### Developer 1
**Morning:**
- [ ] Implement dashboard APIs (admin, instructor, student)
- [ ] Write queries for dashboard statistics
- [ ] Test dashboard endpoints

**Afternoon:**
- [ ] Review frontend integration issues
- [ ] Fix any CORS or authentication problems
- [ ] Add validation to API endpoints

**Evening:**
- [ ] Code review of backend so far
- [ ] Write basic tests for critical endpoints

#### Developer 2
**Morning:**
- [ ] Create AdminEnrollments.vue page
  - [ ] List all students
  - [ ] Enroll student form (select student + batch)

**Afternoon:**
- [ ] Create AdminPayments.vue page
  - [ ] Record payment form
  - [ ] View payment history by student
  - [ ] Show fee status

**Evening:**
- [ ] Create AdminDashboard.vue page
  - [ ] Show statistics cards
  - [ ] Recent enrollments table

---

### **Day 4 (Thursday): Instructor & Student Pages**

#### Developer 1
**Morning:**
- [ ] Help with frontend debugging
- [ ] Add any missing backend validations
- [ ] Optimize database queries

**Afternoon:**
- [ ] Set up database migrations properly
- [ ] Create seed data script for testing
- [ ] Test full enrollment flow

**Evening:**
- [ ] Security review of authentication
- [ ] Ensure passwords are hashed
- [ ] Check JWT token expiration

#### Developer 2
**Morning:**
- [ ] Create InstructorDashboard.vue
  - [ ] Show instructor's batches
  - [ ] Show student count per batch

**Afternoon:**
- [ ] Create InstructorBatches.vue
  - [ ] List instructor's batches
  - [ ] View students in each batch
  
- [ ] Create InstructorAttendance.vue
  - [ ] Select batch and date
  - [ ] Mark attendance for all students (checkboxes)
  - [ ] Submit attendance

**Evening:**
- [ ] Test instructor workflows
- [ ] Fix any bugs

---

### **Day 5 (Friday): Student Pages & Polish**

#### Developer 1
**Morning:**
- [ ] Final backend testing
- [ ] Fix any remaining bugs
- [ ] Add error handling to all routes

**Afternoon:**
- [ ] Write API documentation
- [ ] Test edge cases (see TESTING_SUITE.md)
- [ ] Performance check

**Evening:**
- [ ] Database backup
- [ ] Deployment preparation (optional)

#### Developer 2
**Morning:**
- [ ] Create StudentDashboard.vue
  - [ ] Show enrolled batch info
  - [ ] Show attendance summary
  - [ ] Show fee status

**Afternoon:**
- [ ] Create StudentAttendance.vue
  - [ ] Show attendance history table
  - [ ] Show attendance percentage
  
- [ ] Polish UI across all pages
  - [ ] Consistent styling
  - [ ] Loading states
  - [ ] Error messages

**Evening:**
- [ ] Cross-browser testing
- [ ] Mobile responsiveness check

---

### **Day 6 (Saturday): Integration Testing**

#### Both Developers
**Morning:**
- [ ] Complete user flow testing:
  - [ ] Admin creates course → batch → enrolls student → records payment
  - [ ] Instructor marks attendance
  - [ ] Student views their info

**Afternoon:**
- [ ] Run through TESTING_SUITE.md test cases
- [ ] Fix all critical bugs
- [ ] Document known issues

**Evening:**
- [ ] Code cleanup
- [ ] Remove console.logs
- [ ] Add comments where needed

---

### **Day 7 (Sunday): Final Testing & Demo Prep**

#### Both Developers
**Morning:**
- [ ] Final bug fixes
- [ ] End-to-end testing
- [ ] Prepare demo data

**Afternoon:**
- [ ] Create demo accounts (admin, instructor, student)
- [ ] Prepare demo script
- [ ] Practice presentation

**Evening:**
- [ ] Final deployment (if needed)
- [ ] Documentation review
- [ ] Celebrate! 🎉

---

## 📋 Essential Checklists

### Backend Checklist (Developer 1)
- [ ] All 27 API endpoints working
- [ ] JWT authentication implemented
- [ ] Role-based authorization working
- [ ] Database migrations created
- [ ] Passwords are hashed
- [ ] Input validation on all endpoints
- [ ] Error handling implemented
- [ ] CORS configured properly

### Frontend Checklist (Developer 2)
- [ ] Login/Register pages work
- [ ] 3 admin pages (courses, batches, enrollments, payments, dashboard)
- [ ] 3 instructor pages (dashboard, batches, attendance)
- [ ] 2 student pages (dashboard, attendance)
- [ ] API integration working
- [ ] JWT token stored and sent
- [ ] Role-based routing working
- [ ] Loading states shown
- [ ] Error messages displayed

---

## 🛠️ Tools You'll Need

### Development Tools
- **Code Editor:** VS Code (recommended)
- **API Testing:** Postman or Thunder Client (VS Code extension)
- **Database Tool:** DB Browser for SQLite
- **Version Control:** Git + GitHub

### Communication
- **Daily Standup:** 15 min each morning
- **Shared Doc:** Google Docs for blockers
- **Screen Share:** When stuck on a bug

---

## 🆘 Troubleshooting Common Issues

### "CORS Error"
**Fix:** Add Flask-CORS to backend
```python
from flask_cors import CORS
CORS(app)
```

### "401 Unauthorized"
**Fix:** Check if token is being sent in Authorization header
```javascript
headers: { Authorization: `Bearer ${token}` }
```

### "Foreign Key Constraint Failed"
**Fix:** Ensure related records exist before creating (e.g., course must exist before creating batch)

### "Database Locked" (SQLite)
**Fix:** Close all database connections, restart Flask server

### "Module Not Found"
**Fix:** Activate virtual environment and reinstall requirements
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📊 Progress Tracking

Use this checklist to track your progress:

### Backend APIs (27 endpoints)
- [ ] Auth (4) - register, login, logout, me
- [ ] Users (3) - list, get, update
- [ ] Courses (4) - list, create, get, update
- [ ] Batches (5) - list, create, get, update, students
- [ ] Enrollments (2) - create, get by student
- [ ] Payments (3) - create, get history, get fee status
- [ ] Attendance (3) - mark, get by batch, get by student
- [ ] Dashboards (3) - admin, instructor, student

### Frontend Pages (13 pages)
- [ ] Login & Register (2)
- [ ] Admin (5) - dashboard, courses, batches, enrollments, payments
- [ ] Instructor (3) - dashboard, batches, attendance
- [ ] Student (2) - dashboard, attendance

---

## 💡 Pro Tips

1. **Start Simple:** Get one feature fully working before moving to next
2. **Test Often:** Don't wait until Day 7 to test
3. **Use Postman:** Save all API requests in a collection
4. **Commit Frequently:** Commit working code every few hours
5. **Ask for Help:** If stuck for >1 hour, ask your partner
6. **Take Breaks:** Don't burn out, take regular breaks
7. **Document Issues:** Keep a list of bugs to fix
8. **Use Seed Data:** Create a script to populate test data quickly

---

## 📞 When You Need Help

### Reference Documents
1. Backend stuck? → See `BACKEND_IMPLEMENTATION.md`
2. Frontend stuck? → See `FRONTEND_IMPLEMENTATION.md`
3. API questions? → See `API_SPECIFICATION_MVP.yaml`
4. Testing questions? → See `TESTING_SUITE.md`

### Common Questions

**Q: Should we use TypeScript?**
A: No, use plain JavaScript to save time.

**Q: Should we add tests?**
A: Focus on manual testing for MVP. Automated tests can come later.

**Q: What about deployment?**
A: Run locally for demo. Deploy after MVP works.

**Q: Can we change the scope?**
A: You can simplify further if needed, but don't add features!

---

## ✅ Definition of Done

Your MVP is done when:

1. ✅ You can do this complete flow:
   - Admin creates course "JEE 2024" with fee 50000
   - Admin creates batch "Morning Batch" for that course
   - Student registers account
   - Admin enrolls student in batch
   - Admin records payment of 25000
   - Instructor marks student present
   - Student logs in and sees their attendance and fee status

2. ✅ All 3 role dashboards show correct data

3. ✅ No critical bugs (minor bugs are OK!)

4. ✅ Code is on GitHub

---

## 🎯 Success Criteria

After 1 week, you should have:
- Working web application
- 3 different user experiences (admin, instructor, student)
- Real business value (can actually run a small coaching institute)
- Clean, understandable code
- Ready for user feedback

---

## 🚀 You've Got This!

Remember: The goal is a **working MVP**, not a perfect product. 

Focus on:
- ✅ Making it work
- ✅ Core features only
- ✅ Simple and clean

Don't worry about:
- ❌ Perfect UI
- ❌ Every edge case
- ❌ Performance optimization
- ❌ Fancy features

**Good luck! You can do this in 1 week! 💪**
