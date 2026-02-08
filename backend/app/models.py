from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'instructor', 'student', name='user_roles'), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    taught_batches = db.relationship('Batch', backref='instructor', lazy='dynamic')
    enrollment = db.relationship('Enrollment', backref='student', uselist=False)
    payments = db.relationship('Payment', backref='student', lazy='dynamic')
    attendance_records = db.relationship('Attendance', foreign_keys='Attendance.student_id', backref='student', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'phone': self.phone,
            'created_at': self.created_at.isoformat()
        }


class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    total_fee = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    batches = db.relationship('Batch', backref='course', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'total_fee': float(self.total_fee),
            'created_at': self.created_at.isoformat()
        }


class Batch(db.Model):
    __tablename__ = 'batches'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    batch_name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    schedule_time = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='batch', lazy='dynamic')
    attendance_records = db.relationship('Attendance', backref='batch', lazy='dynamic')
    
    def to_dict(self, include_details=False):
        data = {
            'id': self.id,
            'course_id': self.course_id,
            'instructor_id': self.instructor_id,
            'batch_name': self.batch_name,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'schedule_time': self.schedule_time,
            'created_at': self.created_at.isoformat()
        }
        
        if include_details:
            data['course'] = self.course.to_dict()
            data['instructor'] = self.instructor.to_dict()
        
        return data


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Enum('active', 'completed', 'dropped', name='enrollment_status'), default='active')
    
    def to_dict(self, include_details=False):
        data = {
            'id': self.id,
            'student_id': self.student_id,
            'batch_id': self.batch_id,
            'enrollment_date': self.enrollment_date.isoformat(),
            'status': self.status
        }
        
        if include_details:
            data['batch'] = self.batch.to_dict(include_details=True)
        
        return data


class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_mode = db.Column(db.Enum('cash', 'card', 'upi', 'bank_transfer', name='payment_modes'), default='cash')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'amount': float(self.amount),
            'payment_date': self.payment_date.isoformat(),
            'payment_mode': self.payment_mode,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }


class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('present', 'absent', name='attendance_status'), nullable=False)
    marked_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('batch_id', 'student_id', 'date', name='unique_attendance'),
    )
    
    marker = db.relationship('User', foreign_keys=[marked_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'batch_id': self.batch_id,
            'student_id': self.student_id,
            'date': self.date.isoformat(),
            'status': self.status,
            'marked_by': self.marked_by,
            'created_at': self.created_at.isoformat()
        }
