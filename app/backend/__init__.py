from flask import Blueprint

backend = Blueprint('backend', __name__)

from . import views