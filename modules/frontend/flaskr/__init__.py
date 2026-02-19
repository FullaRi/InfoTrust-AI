import os
from flask import Flask
from . import flask_config
from setup import settings
from flask_wtf.csrf import CSRFProtect
from flask_mailman import Mail

def create_app():
    # create and configure the app
    app = Flask(
        __name__,
        template_folder=flask_config.TEMPLATE_FOLDER,
        static_folder=flask_config.STATIC_FOLDER
    )

    if settings.DEBUG is True:
        app.config.from_object(flask_config.DevelopmentConfig)
    else:
        app.config.from_object(flask_config.ProductionConfig)

    # Initialize Flask extensions
    mail = Mail(app)
    csrf = CSRFProtect(app)

    # Register blueprints
    from . import core
    app.register_blueprint(core.bp)

    return app