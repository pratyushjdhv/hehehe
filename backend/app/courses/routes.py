from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.courses import bp
from app.models import Course, User

def require_admin():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return user and user.role == 'admin'


@bp.route('', methods=['GET'])
@jwt_required()
def get_courses():
    courses = Course.query.all()
    return jsonify({
        'courses': [course.to_dict() for course in courses]
    }), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_course():
    if not require_admin():
        return jsonify({'message': 'Forbidden'}), 403
    
    data = request.get_json()
    
    if 'name' not in data or 'total_fee' not in data:
        return jsonify({'message': 'name and total_fee are required'}), 400
    
    course = Course(
        name=data['name'],
        description=data.get('description'),
        total_fee=data['total_fee']
    )
    
    db.session.add(course)
    db.session.commit()
    
    return jsonify(course.to_dict()), 201


@bp.route('/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course(course_id):
    course = Course.query.get(course_id)
    
    if not course:
        return jsonify({'message': 'Course not found'}), 404
    
    return jsonify(course.to_dict()), 200


@bp.route('/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    if not require_admin():
        return jsonify({'message': 'Forbidden'}), 403
    
    course = Course.query.get(course_id)
    
    if not course:
        return jsonify({'message': 'Course not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        course.name = data['name']
    if 'description' in data:
        course.description = data['description']
    if 'total_fee' in data:
        course.total_fee = data['total_fee']
    
    db.session.commit()
    
    return jsonify(course.to_dict()), 200
