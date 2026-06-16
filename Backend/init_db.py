from app import create_app
from app.models.db import db
from app.models.prediction_history import PredictionHistory

app = create_app()

with app.app_context():
    db.create_all()
    print("Database + Tables created successfully!")