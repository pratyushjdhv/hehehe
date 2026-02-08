# CoachMaster Backend API

Flask-based REST API for coaching institute management system.

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and update the secret keys (optional for development, required for production).

### 4. Initialize Database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/logout` - Logout user

### Users
- `GET /api/v1/users` - List users (admin only)
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user

### Courses
- `GET /api/v1/courses` - List courses
- `POST /api/v1/courses` - Create course (admin only)
- `GET /api/v1/courses/{id}` - Get course
- `PUT /api/v1/courses/{id}` - Update course (admin only)

### Batches
- `GET /api/v1/batches` - List batches
- `POST /api/v1/batches` - Create batch (admin only)
- `GET /api/v1/batches/{id}` - Get batch
- `PUT /api/v1/batches/{id}` - Update batch (admin only)
- `GET /api/v1/batches/{id}/students` - Get students in batch

### Enrollments
- `POST /api/v1/enrollments` - Enroll student (admin only)
- `GET /api/v1/students/{id}/enrollment` - Get student enrollment

### Payments
- `POST /api/v1/payments` - Record payment (admin only)
- `GET /api/v1/students/{id}/payments` - Get student payments
- `GET /api/v1/students/{id}/fee-status` - Get student fee status

### Attendance
- `POST /api/v1/attendance` - Mark attendance (instructor/admin)
- `GET /api/v1/batches/{id}/attendance` - Get batch attendance
- `GET /api/v1/students/{id}/attendance` - Get student attendance

### Dashboard
- `GET /api/v1/dashboard/admin` - Admin dashboard (admin only)
- `GET /api/v1/dashboard/instructor` - Instructor dashboard (instructor only)
- `GET /api/v1/dashboard/student` - Student dashboard (student only)

## Testing the API

### Using curl

Register a user:
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "password123",
    "full_name": "Admin User",
    "role": "admin"
  }'
```

Login:
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "password123"
  }'
```

Use the token from login response for authenticated requests:
```bash
curl -X GET http://localhost:5000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py            # Configuration
│   ├── models.py            # Database models
│   ├── auth/                # Authentication module
│   ├── users/               # User management
│   ├── courses/             # Course management
│   ├── batches/             # Batch management
│   ├── enrollments/         # Enrollment management
│   ├── payments/            # Payment management
│   ├── attendance/          # Attendance management
│   └── dashboard/           # Dashboard endpoints
├── migrations/              # Database migrations
├── tests/                   # Test files
├── requirements.txt         # Dependencies
├── .env.example            # Example environment file
├── .gitignore              # Git ignore rules
└── run.py                  # Application entry point
```

## Database Models

- **User** - Users (admin, instructor, student)
- **Course** - Available courses
- **Batch** - Course batches with instructor
- **Enrollment** - Student enrollment in batch
- **Payment** - Fee payments
- **Attendance** - Attendance records

## Development Tips

1. **Create seed data** - Create a script to populate test data
2. **Use Postman** - Import the OpenAPI spec for easy testing
3. **Check logs** - Monitor the console for errors
4. **Database browser** - Use DB Browser for SQLite to inspect data

## Common Issues

### "Table doesn't exist"
Run database migrations:
```bash
flask db upgrade
```

### "Module not found"
Activate virtual environment and reinstall:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "CORS Error"
CORS is enabled by default. Check frontend is making requests to correct URL.

### "401 Unauthorized"
Ensure JWT token is included in Authorization header: `Bearer YOUR_TOKEN`
