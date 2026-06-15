import pandas as pd
import numpy as np
import joblib
import os
from flask import Blueprint, request, jsonify
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "models",
    "random_forest.pkl"
)

model = joblib.load(MODEL_PATH)

from app.utils.schema import MODEL_FEATURES
from app.utils.validator import validate_input_data
from app.utils.mapping_engine import smart_match_columns
from app.utils.pipeline import get_preprocessor

upload_bp = Blueprint("upload_bp", __name__)

# Load model
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "random_forest.pkl")
model = joblib.load(MODEL_PATH)


@upload_bp.route("/upload", methods=["POST"])
def upload_csv():
    try:
        # STEP 1: Read file
        file = request.files["file"]
        df = pd.read_csv(file)

        # STEP 2: Extract CSV columns
        csv_columns = list(df.columns)

        # STEP 3: Smart column mapping
        mapping = smart_match_columns(csv_columns, MODEL_FEATURES)

        # STEP 4: Build model input dataframe
        input_data = pd.DataFrame()

        missing_features = []

        for feature in MODEL_FEATURES:
            col_name = mapping.get(feature)

            if col_name:
                input_data[feature] = df[col_name]
            else:
                # fallback value (safe default)
                input_data[feature] = 0
                missing_features.append(feature)

        # STEP 5: VALIDATION (IMPORTANT)
        valid, validation_msg = validate_input_data(input_data, MODEL_FEATURES)

        if not valid:
            return jsonify({
                "status": "error",
                "message": "Validation failed",
                "details": validation_msg
            }), 400
        preprocessor = get_preprocessor()

        input_scaled = preprocessor.fit_transform(input_data)


        # STEP 6: Prediction
        predictions = model.predict(input_scaled)
        probabilities = model.predict_proba(input_scaled)[:, 1]

        # STEP 7: Prepare output
        result_df = df.copy()
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