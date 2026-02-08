from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.users import bp
from app.models import User

def require_admin():
    """Check if current user is admin"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return user and user.role == 'admin'


@bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    if not require_admin():
        return jsonify({'message': 'Forbidden'}), 403
    
    role_filter = request.args.get('role')
    
    query = User.query
    if role_filter and role_filter in ['admin', 'instructor', 'student']:
        query = query.filter_by(role=role_filter)
    
    users = query.all()
    
    return jsonify({
        'users': [user.to_dict() for user in users]
    }), 200


@bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Only admin can update other users, users can update themselves
    if current_user.role != 'admin' and current_user_id != user_id:
        return jsonify({'message': 'Forbidden'}), 403
    
    data = request.get_json()
    
    # Update allowed fields
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'phone' in data:
        user.phone = data['phone']
    if 'email' in data and current_user.role == 'admin':
        # Check if email is unique
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'message': 'Email already exists'}), 400
        user.email = data['email']
    
    db.session.commit()
    
    return jsonify(user.to_dict()), 200
