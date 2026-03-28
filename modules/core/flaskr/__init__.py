import os
from flask import Flask, request, make_response
from . import flask_config
from setup import settings
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

def create_app():
    # create and configure the app
    app = Flask(
        __name__,
        # template_folder=flask_config.TEMPLATE_FOLDER,
        # static_folder=flask_config.STATIC_FOLDER
    )

    if settings.DEBUG is True:
        app.config.from_object(flask_config.DevelopmentConfig)
    else:
        app.config.from_object(flask_config.ProductionConfig)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # 2. Ajoutez ce "HACK" de sécurité pour forcer le 200 OK sur OPTIONS
    # Cela évite que vos routes ou middlewares ne renvoient une 400
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            res = make_response()
            res.headers.add("Access-Control-Allow-Origin", "*")
            res.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
            res.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            res.headers.add("Access-Control-Allow-Credentials", "true")
            return res, 200

    # Initialize Flask extensions
    # csrf = CSRFProtect(app)

    # Register blueprints
    from . import core
    app.register_blueprint(core.bp)

    return app