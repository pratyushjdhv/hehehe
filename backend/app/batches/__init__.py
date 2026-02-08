from flask import Blueprint

bp = Blueprint('batches', __name__)

from app.batches import routes
