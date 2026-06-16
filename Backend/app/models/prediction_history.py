from datetime import datetime
from app.models.db import db

class PredictionHistory(db.Model):
    __tablename__ = "prediction_history"

    id = db.Column(db.Integer, primary_key=True)

    customer_data = db.Column(db.Text, nullable=False)  # JSON string of input

    prediction = db.Column(db.String(50), nullable=False)  # "Churn" or "No Churn"

    probability = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)