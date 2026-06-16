import pandas as pd
import numpy as np
import joblib
import os
from flask import Blueprint, request, jsonify

from app.utils.schema import MODEL_FEATURES
from app.utils.validator import validate_input_data
from app.utils.mapping_engine import smart_match_columns

upload_bp = Blueprint("upload_bp", __name__)

# -------------------------------
# LOAD MODEL (ONLY ONCE)
# -------------------------------
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "models",
    "random_forest.pkl"
)

model = joblib.load(MODEL_PATH)


# -------------------------------
# ENCODING FIX FUNCTION
# -------------------------------
def preprocess_data(df):
    df = df.copy()

    # Clean column names
    df.columns = df.columns.str.strip()

    # Contract type encoding
    df["contract_type"] = df["contract_type"].astype(str).str.strip().replace({
        "Month-to-month": 0,
        "One year": 1,
        "Two year": 2
    })

    # Gender encoding
    if "gender" in df.columns:
        df["gender"] = df["gender"].astype(str).str.strip().replace({
            "Male": 1,
            "Female": 0
        })

    # SeniorCitizen fix
    if "SeniorCitizen" in df.columns:
        df["SeniorCitizen"] = df["SeniorCitizen"].replace({
            "Yes": 1,
            "No": 0
        })

    # Convert everything safely
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fill missing values
    df = df.fillna(0)

    return df
# -------------------------------
# ROUTE
# -------------------------------
@upload_bp.route("/upload", methods=["POST"])
def upload_csv():
    try:
        # STEP 1: Read file
        file = request.files["file"]
        df = pd.read_csv(file)

        # STEP 2: Smart mapping
        mapping = smart_match_columns(list(df.columns), MODEL_FEATURES)

        input_data = pd.DataFrame()
        missing_features = []

        # STEP 3: Build model input
        for feature in MODEL_FEATURES:
            col_name = mapping.get(feature)

            if col_name:
                input_data[feature] = df[col_name]
            else:
                input_data[feature] = 0
                missing_features.append(feature)

        # STEP 4: VALIDATION
        print("⚠️ Validation temporarily disabled for debugging")

        # STEP 5: 🔥 FIX (ENCODING)
        input_data = preprocess_data(input_data)
        print("🔥 DEBUG INPUT DATA")
        print(input_data.head())
        print(input_data.dtypes)

        # STEP 6: PREDICTION (NO SCALING, NO FIT_TRANSFORM)
        predictions = model.predict(input_data)
        probabilities = model.predict_proba(input_data)[:, 1]

        # STEP 7: RESPONSE
        result_df = input_data.copy()
        result_df["prediction"] = predictions
        result_df["churn_probability"] = probabilities

        return jsonify({
            "status": "success",
            "rows_processed": len(df),
            "mapping_used": mapping,
            "missing_features_filled": missing_features,
            "sample_output": result_df.head(5).to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500