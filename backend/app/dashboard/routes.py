from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from app.dashboard import bp
from app.models import User, Course, Batch, Enrollment, Payment, Attendance

def require_role(role):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return user and user.role == role


@bp.route('/admin', methods=['GET'])
@jwt_required()
def get_admin_dashboard():
    if not require_role('admin'):
        return jsonify({'message': 'Forbidden'}), 403
    
    from app import db
    
    total_students = User.query.filter_by(role='student').count()
    total_instructors = User.query.filter_by(role='instructor').count()
    total_courses = Course.query.count()
    total_batches = Batch.query.count()
    
    total_revenue = db.session.query(func.sum(Payment.amount)).scalar() or 0
    
    # Get recent enrollments (last 5)
    recent_enrollments = Enrollment.query.order_by(Enrollment.enrollment_date.desc()).limit(5).all()
    
    recent_enrollments_data = []
    for enrollment in recent_enrollments:
        recent_enrollments_data.append({
            'student_name': enrollment.student.full_name,
            'batch_name': enrollment.batch.batch_name,
            'enrollment_date': enrollment.enrollment_date.isoformat()
        })
    
    return jsonify({
        'total_students': total_students,
        'total_instructors': total_instructors,
        'total_courses': total_courses,
        'total_batches': total_batches,
        'total_revenue': float(total_revenue),
        'recent_enrollments': recent_enrollments_data
    }), 200


@bp.route('/instructor', methods=['GET'])
@jwt_required()
def get_instructor_dashboard():
    current_user_id = get_jwt_identity()
    
    if not require_role('instructor'):
        return jsonify({'message': 'Forbidden'}), 403
    
    user = User.query.get(current_user_id)
    
    batches = Batch.query.filter_by(instructor_id=current_user_id).all()
    
    total_batches = len(batches)
    
    # Count total students across all batches
    total_students = 0
    batch_data = []
    
    for batch in batches:
        student_count = Enrollment.query.filter_by(batch_id=batch.id).count()
        total_students += student_count
        
        batch_data.append({
            'batch_id': batch.id,
            'batch_name': batch.batch_name,
            'course_name': batch.course.name,
            'student_count': student_count,
            'schedule_time': batch.schedule_time
        })
    
    return jsonify({
        'instructor_name': user.full_name,
        'total_batches': total_batches,
        'total_students': total_students,
        'my_batches': batch_data
    }), 200


@bp.route('/student', methods=['GET'])
@jwt_required()
def get_student_dashboard():
    current_user_id = get_jwt_identity()
    
    if not require_role('student'):
        return jsonify({'message': 'Forbidden'}), 403
    
    user = User.query.get(current_user_id)
    
    # Get enrollment
    enrollment = Enrollment.query.filter_by(student_id=current_user_id).first()
    
    enrolled_batch = None
    attendance_summary = None
    fee_status = None
    
    if enrollment:
        batch = enrollment.batch
        enrolled_batch = {
            'batch_id': batch.id,
            'batch_name': batch.batch_name,
            'course_name': batch.course.name,
            'instructor_name': batch.instructor.full_name,
            'schedule_time': batch.schedule_time
        }
        
        # Get attendance summary
        attendance_records = Attendance.query.filter_by(student_id=current_user_id).all()
        total_classes = len(attendance_records)
        present_count = len([r for r in attendance_records if r.status == 'present'])
        attendance_percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
        
        attendance_summary = {
            'total_classes': total_classes,
            'present_count': present_count,
            'attendance_percentage': round(attendance_percentage, 2)
        }
        
        # Get fee status
        from app import db
        total_paid = db.session.query(func.sum(Payment.amount)).filter_by(student_id=current_user_id).scalar() or 0
        total_fee = batch.course.total_fee
        
        fee_status = {
            'total_fee': float(total_fee),
            'paid': float(total_paid),
            'balance': float(total_fee) - float(total_paid)
        }
    
    return jsonify({
        'student_name': user.full_name,
        'enrolled_batch': enrolled_batch,
        'attendance_summary': attendance_summary,
        'fee_status': fee_status
    }), 200
