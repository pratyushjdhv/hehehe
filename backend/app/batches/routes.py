from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.batches import bp
from app.models import Batch, Course, User, Enrollment

def require_admin():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return user and user.role == 'admin'


@bp.route('', methods=['GET'])
@jwt_required()
def get_batches():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    course_id = request.args.get('course_id', type=int)
    
    query = Batch.query
    
    # Instructors can only see their own batches
    if current_user.role == 'instructor':
        query = query.filter_by(instructor_id=current_user_id)
    
    # Filter by course if provided
    if course_id:
        query = query.filter_by(course_id=course_id)
    
    batches = query.all()
    
    return jsonify({
        'batches': [batch.to_dict() for batch in batches]
    }), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_batch():
    if not require_admin():
        return jsonify({'message': 'Forbidden'}), 403
    
    data = request.get_json()
    
    required_fields = ['course_id', 'instructor_id', 'batch_name', 'start_date', 'schedule_time']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'{field} is required'}), 400
    
    # Validate course exists
    course = Course.query.get(data['course_id'])
    if not course:
        return jsonify({'message': 'Course not found'}), 400
    
    # Validate instructor exists and has instructor role
    instructor = User.query.get(data['instructor_id'])
    if not instructor or instructor.role != 'instructor':
        return jsonify({'message': 'Instructor not found'}), 400
    
    batch = Batch(
        course_id=data['course_id'],
        instructor_id=data['instructor_id'],
        batch_name=data['batch_name'],
        start_date=datetime.fromisoformat(data['start_date']).date(),
        end_date=datetime.fromisoformat(data['end_date']).date() if data.get('end_date') else None,
        schedule_time=data['schedule_time']
    )
    
    db.session.add(batch)
    db.session.commit()
    
    return jsonify(batch.to_dict()), 201


@bp.route('/<int:batch_id>', methods=['GET'])
@jwt_required()
def get_batch(batch_id):
    batch = Batch.query.get(batch_id)
    
    if not batch:
        return jsonify({'message': 'Batch not found'}), 404
    
    return jsonify(batch.to_dict(include_details=True)), 200


@bp.route('/<int:batch_id>', methods=['PUT'])
@jwt_required()
def update_batch(batch_id):
    if not require_admin():
        return jsonify({'message': 'Forbidden'}), 403
    
    batch = Batch.query.get(batch_id)
    
    if not batch:
        return jsonify({'message': 'Batch not found'}), 404
    
    data = request.get_json()
    
    if 'batch_name' in data:
        batch.batch_name = data['batch_name']
    if 'instructor_id' in data:
        instructor = User.query.get(data['instructor_id'])
        if not instructor or instructor.role != 'instructor':
            return jsonify({'message': 'Instructor not found'}), 400
        batch.instructor_id = data['instructor_id']
    if 'start_date' in data:
        batch.start_date = datetime.fromisoformat(data['start_date']).date()
    if 'end_date' in data:
        batch.end_date = datetime.fromisoformat(data['end_date']).date() if data['end_date'] else None
    if 'schedule_time' in data:
        batch.schedule_time = data['schedule_time']
    
    db.session.commit()
    
    return jsonify(batch.to_dict()), 200


@bp.route('/<int:batch_id>/students', methods=['GET'])
@jwt_required()
def get_batch_students(batch_id):
    batch = Batch.query.get(batch_id)
    
    if not batch:
        return jsonify({'message': 'Batch not found'}), 404
    
    enrollments = Enrollment.query.filter_by(batch_id=batch_id).all()
    
    students = []
    for enrollment in enrollments:
        student_data = enrollment.student.to_dict()
        student_data['enrollment_id'] = enrollment.id
        student_data['enrollment_date'] = enrollment.enrollment_date.isoformat()
        student_data['enrollment_status'] = enrollment.status
        students.append(student_data)
    
    return jsonify({
        'students': students
    }), 200
