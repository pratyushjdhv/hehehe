from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from sqlalchemy import func
from app import db
from app.attendance import bp
from app.models import Attendance, User, Batch, Enrollment

def is_instructor_or_admin():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return user and user.role in ['admin', 'instructor']


@bp.route('/attendance', methods=['POST'])
@jwt_required()
def mark_attendance():
    if not is_instructor_or_admin():
        return jsonify({'message': 'Forbidden'}), 403
    
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['batch_id', 'date', 'attendance_records']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'{field} is required'}), 400
    
    batch = Batch.query.get(data['batch_id'])
    if not batch:
        return jsonify({'message': 'Batch not found'}), 400
    
    attendance_date = datetime.fromisoformat(data['date']).date()
    
    # Validate all students are in the batch
    batch_student_ids = [e.student_id for e in Enrollment.query.filter_by(batch_id=data['batch_id']).all()]
    
    records_created = 0
    for record in data['attendance_records']:
        if record['student_id'] not in batch_student_ids:
            return jsonify({'message': f"Student {record['student_id']} not enrolled in this batch"}), 400
        
        # Check if attendance already marked
        existing = Attendance.query.filter_by(
            batch_id=data['batch_id'],
            student_id=record['student_id'],
            date=attendance_date
        ).first()
        
        if existing:
            return jsonify({'message': f"Attendance already marked for this date"}), 400
        
        attendance = Attendance(
            batch_id=data['batch_id'],
            student_id=record['student_id'],
            date=attendance_date,
            status=record['status'],
            marked_by=current_user_id
        )
        db.session.add(attendance)
        records_created += 1
    
    db.session.commit()
    
    return jsonify({
        'message': 'Attendance marked successfully',
        'records_created': records_created
    }), 201


@bp.route('/batches/<int:batch_id>/attendance', methods=['GET'])
@jwt_required()
def get_batch_attendance(batch_id):
    batch = Batch.query.get(batch_id)
    
    if not batch:
        return jsonify({'message': 'Batch not found'}), 404
    
    query = Attendance.query.filter_by(batch_id=batch_id)
    
    # Filter by date if provided
    date_filter = request.args.get('date')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if date_filter:
        query = query.filter_by(date=datetime.fromisoformat(date_filter).date())
    elif start_date and end_date:
        query = query.filter(
            Attendance.date >= datetime.fromisoformat(start_date).date(),
            Attendance.date <= datetime.fromisoformat(end_date).date()
        )
    
    attendance_records = query.all()
    
    results = []
    for record in attendance_records:
        data = record.to_dict()
        data['student_name'] = record.student.full_name
        results.append(data)
    
    return jsonify({
        'batch_id': batch_id,
        'batch_name': batch.batch_name,
        'attendance': results
    }), 200


@bp.route('/students/<int:student_id>/attendance', methods=['GET'])
@jwt_required()
def get_student_attendance(student_id):
    student = User.query.get(student_id)
    
    if not student or student.role != 'student':
        return jsonify({'message': 'Student not found'}), 404
    
    attendance_records = Attendance.query.filter_by(student_id=student_id).all()
    
    total_classes = len(attendance_records)
    present_count = len([r for r in attendance_records if r.status == 'present'])
    absent_count = len([r for r in attendance_records if r.status == 'absent'])
    attendance_percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
    
    # Get recent attendance (last 10 records)
    recent_attendance = sorted(attendance_records, key=lambda x: x.date, reverse=True)[:10]
    
    return jsonify({
        'student_id': student_id,
        'student_name': student.full_name,
        'total_classes': total_classes,
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_percentage': round(attendance_percentage, 2),
        'recent_attendance': [
            {
                'date': r.date.isoformat(),
                'status': r.status
            } for r in recent_attendance
        ]
    }), 200
