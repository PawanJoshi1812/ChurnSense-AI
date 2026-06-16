import joblib
import numpy as np
import os

MODEL_PATH = os.path.join("models", "random_forest.pkl")

model = joblib.load(MODEL_PATH)

def predict_churn(data):
    """
    data = list of features in correct order:
    [tenure, monthly_charges, total_charges,
     support_tickets, contract_type, payment_delay]
    """

    input_array = np.array([data])

    prediction = model.predict(input_array)[0]
    probability = model.predict_proba(input_array)[0][1]

    return {
        "prediction": int(prediction),
        "prediction_label": "Churn" if prediction == 1 else "Not Churn",
        "churn_probability": float(probability)
    }