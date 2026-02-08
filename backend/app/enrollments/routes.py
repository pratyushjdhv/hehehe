from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.enrollments import bp
from app.models import Enrollment, User, Batch

def require_admin():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return user and user.role == 'admin'


@bp.route('/enrollments', methods=['POST'])
@jwt_required()
def create_enrollment():
    if not require_admin():
        return jsonify({'message': 'Forbidden'}), 403
    
    data = request.get_json()
    
    if 'student_id' not in data or 'batch_id' not in data:
        return jsonify({'message': 'student_id and batch_id are required'}), 400
    
    # Validate student exists and has student role
    student = User.query.get(data['student_id'])
    if not student or student.role != 'student':
        return jsonify({'message': 'Student not found'}), 400
    
    # Validate batch exists
    batch = Batch.query.get(data['batch_id'])
    if not batch:
        return jsonify({'message': 'Batch not found'}), 400
    
    # Check if student is already enrolled
    existing_enrollment = Enrollment.query.filter_by(student_id=data['student_id']).first()
    if existing_enrollment:
        return jsonify({'message': 'Student already enrolled in a batch'}), 400
    
    enrollment = Enrollment(
        student_id=data['student_id'],
        batch_id=data['batch_id'],
        enrollment_date=datetime.utcnow().date()
    )
    
    db.session.add(enrollment)
    db.session.commit()
    
    return jsonify(enrollment.to_dict()), 201


@bp.route('/students/<int:student_id>/enrollment', methods=['GET'])
@jwt_required()
def get_student_enrollment(student_id):
    enrollment = Enrollment.query.filter_by(student_id=student_id).first()
    
    if not enrollment:
        return jsonify({'message': 'No enrollment found for this student'}), 404
    
    return jsonify(enrollment.to_dict(include_details=True)), 200
