import pandas as pd
from sklearn.preprocessing import LabelEncoder
from app.services.prediction_service import predict_churn

# IMPORTANT: same encoding logic as training
le = LabelEncoder()
le.fit(["month-to-month", "one_year", "two_year"])

def process_csv(file_path):
    df = pd.read_csv(file_path)

    results = []

    for _, row in df.iterrows():

        contract_encoded = le.transform([row["contract_type"]])[0]

        features = [
            row["tenure"],
            row["monthly_charges"],
            row["total_charges"],
            row["support_tickets"],
            contract_encoded,
            row["payment_delay"]
        ]

        result = predict_churn(features)

        results.append({
    "input": [float(x) for x in features],
    "prediction": "Churn" if int(result["prediction"]) == 1 else "No Churn",
    "probability": float(result["probability"])
})

    return results