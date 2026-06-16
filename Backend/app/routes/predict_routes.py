from flask import Blueprint, request, jsonify
from app.services.prediction_service import predict_churn
from app.services.history_service import save_prediction

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        features = request.json["features"]

        result = predict_churn(features)

        # Save prediction history
        save_prediction(features, result)

        return jsonify({
            "success": True,
            "prediction": result["prediction"],
            "prediction_label": result["prediction_label"],
            "churn_probability": round(result["churn_probability"], 2)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500