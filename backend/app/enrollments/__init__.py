from flask import Blueprint

bp = Blueprint('enrollments', __name__)

from app.enrollments import routes
