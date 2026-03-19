from flask import Blueprint

bp = Blueprint('core', __name__, url_prefix='/')

from flaskr.core import routes