from flask import Blueprint, request, jsonify
from app.services.prediction_service import predict_churn
from app.services.history_service import save_prediction

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json.get("features", None)

        if not data:
            return jsonify({
                "success": False,
                "error": "No features provided"
            }), 400

        result = predict_churn(data)

        # Save history (non-blocking)
        save_prediction(data, result)

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