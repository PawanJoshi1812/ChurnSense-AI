from app.models.db import db
from app.models.prediction_history import PredictionHistory
import json

def save_prediction(input_data, result):
    record = PredictionHistory(
        customer_data=json.dumps(input_data),
        prediction="Churn" if result["prediction"] == 1 else "No Churn",
        probability=result["probability"]
    )

    db.session.add(record)
    db.session.commit()

    return record