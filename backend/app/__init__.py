from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    
    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    
    from app.courses import bp as courses_bp
    app.register_blueprint(courses_bp, url_prefix='/api/v1/courses')
    
    from app.batches import bp as batches_bp
    app.register_blueprint(batches_bp, url_prefix='/api/v1/batches')
    
    from app.enrollments import bp as enrollments_bp
    app.register_blueprint(enrollments_bp, url_prefix='/api/v1')
    
    from app.payments import bp as payments_bp
    app.register_blueprint(payments_bp, url_prefix='/api/v1')
    
    from app.attendance import bp as attendance_bp
    app.register_blueprint(attendance_bp, url_prefix='/api/v1')
    
    from app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/api/v1/dashboard')
    
    return app
