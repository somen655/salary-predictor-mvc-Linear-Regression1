# app/__init__.py
from flask import Flask
from .controllers.api_controller import api_bp
from .controllers.home_controller import home_bp
from .models.regression import ModelRegistry

def create_app():
    app = Flask(__name__)
    app.config["MODEL_VERSION"] = "1.0.0"

    # Lazy-load model on first request
    @app.before_request
    def _ensure_model_loaded():
        if not ModelRegistry.is_loaded():
            ModelRegistry.load()

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app

# Top-level Flask instance for Gunicorn
app = create_app()
