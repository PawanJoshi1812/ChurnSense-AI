import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask
from flask_cors import CORS
from app.models.db import db
from config import Config

def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # Initialize DB
    db.init_app(app)

    with app.app_context():
        from app.models.prediction_history import PredictionHistory 
        db.create_all()

    # Register Blueprints (we already created one)
    from app.routes.health_routes import health_bp
    app.register_blueprint(health_bp)

    from app.routes.predict_routes import predict_bp
    app.register_blueprint(predict_bp)

    from app.routes.history_routes import history_bp
    app.register_blueprint(history_bp)

    from app.routes.upload_routes import upload_bp
    app.register_blueprint(upload_bp)

    from app.routes.explain_routes import explain_bp
    app.register_blueprint(explain_bp)

    return app