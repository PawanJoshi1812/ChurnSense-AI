import os
import joblib
import numpy as np
from flask import Blueprint, request, jsonify

from app.utils.schema import MODEL_FEATURES

from app.utils.schema import MODEL_FEATURES

explain_bp = Blueprint("explain_bp", __name__)

# Load model
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "models",
    "random_forest.pkl"
)

model = joblib.load(MODEL_PATH)


@explain_bp.route("/explain", methods=["POST"])
def explain_prediction():
    try:
        data = request.json

        features = data.get("features")

        if not features or len(features) != len(MODEL_FEATURES):
            return jsonify({
                "status": "error",
                "message": "Invalid input features"
            }), 400

        input_array = np.array(features).reshape(1, -1)

        prediction = model.predict(input_array)[0]
        probability = model.predict_proba(input_array)[0][1]

        # Feature importance (simple version)
        importances = model.feature_importances_

        feature_scores = []

        for i in range(len(MODEL_FEATURES)):
            feature_scores.append({
                "feature": MODEL_FEATURES[i],
                "importance": float(importances[i]),
                "value": float(features[i])
            })

        feature_scores = sorted(
            feature_scores,
            key=lambda x: x["importance"],
            reverse=True
        )

        return jsonify({
            "status": "success",
            "prediction": int(prediction),
            "probability": float(probability),
            "top_factors": feature_scores[:3]
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500