from flask import Blueprint
from flask_cors import CORS

bp = Blueprint('core', __name__, url_prefix='/')

from flaskr.core import routes