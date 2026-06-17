from app.models.db import db
from app.models.prediction_history import PredictionHistory
import json

def save_prediction(input_data, result):
    try:
        record = PredictionHistory(
            customer_data=json.dumps(input_data),
            prediction=result.get("prediction_label", "Unknown"),
            probability=result.get("churn_probability", 0.0)
        )

        db.session.add(record)
        db.session.commit()

        return record

    except Exception as e:
        # Do NOT crash API if history fails
        db.session.rollback()
        print("History save failed:", str(e))
        return None