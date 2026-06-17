import joblib
import numpy as np
import os

MODEL_PATH = os.path.join("models", "random_forest.pkl")
model = joblib.load(MODEL_PATH)

def predict_churn(data):
    try:
        # Validate input
        if not data or len(data) != 6:
            return {
                "prediction": 0,
                "prediction_label": "Invalid Input",
                "churn_probability": 0.0
            }

        # Convert safely
        input_array = np.array([data], dtype=float)

        # Handle NaN / inf
        if np.isnan(input_array).any() or np.isinf(input_array).any():
            return {
                "prediction": 0,
                "prediction_label": "Invalid Input",
                "churn_probability": 0.0
            }

        prediction = model.predict(input_array)[0]
        probability = model.predict_proba(input_array)[0][1]

        return {
            "prediction": int(prediction),
            "prediction_label": "Churn" if prediction == 1 else "Not Churn",
            "churn_probability": float(probability)
        }

    except Exception as e:
        return {
            "prediction": 0,
            "prediction_label": "Error",
            "churn_probability": 0.0
        }