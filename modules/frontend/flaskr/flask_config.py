import os
from pathlib import Path
from setup import settings

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_FOLDER = Path.joinpath(BASE_DIR, 'templates')
STATIC_FOLDER = Path.joinpath(BASE_DIR, 'static')


class Config:
    SECRET_KEY = settings.SECRET_KEY
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
    #     or 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = settings.MAIL_SERVER
    MAIL_PORT = settings.MAIL_PORT
    MAIL_USERNAME = settings.MAIL_USERNAME
    MAIL_PASSWORD = settings.MAIL_PASSWORD
    MAIL_USE_TLS = settings.MAIL_USE_TLS
    MAIL_USE_SSL = settings.MAIL_USE_SSL
    MAIL_DEBUG = settings.MAIL_DEBUG



class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True