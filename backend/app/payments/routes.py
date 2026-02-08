from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from sqlalchemy import func
from app import db
from app.payments import bp
from app.models import Payment, User, Enrollment

def require_admin():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return user and user.role == 'admin'


@bp.route('/payments', methods=['POST'])
@jwt_required()
def create_payment():
    if not require_admin():
        return jsonify({'message': 'Forbidden'}), 403
    
    data = request.get_json()
    
    required_fields = ['student_id', 'amount', 'payment_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'{field} is required'}), 400
    
    # Validate student exists
    student = User.query.get(data['student_id'])
    if not student or student.role != 'student':
        return jsonify({'message': 'Student not found'}), 400
    
    # Validate amount is positive
    if float(data['amount']) <= 0:
        return jsonify({'message': 'Amount must be positive'}), 400
    
    payment = Payment(
        student_id=data['student_id'],
        amount=data['amount'],
        payment_date=datetime.fromisoformat(data['payment_date']).date(),
        payment_mode=data.get('payment_mode', 'cash'),
        notes=data.get('notes')
    )
    
    db.session.add(payment)
    db.session.commit()
    
    return jsonify(payment.to_dict()), 201


@bp.route('/students/<int:student_id>/payments', methods=['GET'])
@jwt_required()
def get_student_payments(student_id):
    payments = Payment.query.filter_by(student_id=student_id).all()
    
    total_paid = db.session.query(func.sum(Payment.amount)).filter_by(student_id=student_id).scalar() or 0
    
    return jsonify({
        'payments': [payment.to_dict() for payment in payments],
        'total_paid': float(total_paid)
    }), 200


@bp.route('/students/<int:student_id>/fee-status', methods=['GET'])
@jwt_required()
def get_fee_status(student_id):
    # Get student enrollment
    enrollment = Enrollment.query.filter_by(student_id=student_id).first()
    
    if not enrollment:
        return jsonify({'message': 'Student not enrolled in any batch'}), 404
    
    # Get total fee from course
    total_fee = enrollment.batch.course.total_fee
    
    # Get total paid
    total_paid = db.session.query(func.sum(Payment.amount)).filter_by(student_id=student_id).scalar() or 0
    
    balance = float(total_fee) - float(total_paid)
    
    student = User.query.get(student_id)
    
    return jsonify({
        'student_id': student_id,
        'student_name': student.full_name,
        'course_name': enrollment.batch.course.name,
        'total_fee': float(total_fee),
        'total_paid': float(total_paid),
        'balance': balance
    }), 200
