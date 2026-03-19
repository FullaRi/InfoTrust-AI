import os
from pathlib import Path
from setup import settings

BASE_DIR = Path(__file__).resolve().parent.parent

# TEMPLATE_FOLDER = Path.joinpath(BASE_DIR, 'templates')
# STATIC_FOLDER = Path.joinpath(BASE_DIR, 'static')


class Config:
    SECRET_KEY = settings.SECRET_KEY
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
    #     or 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True