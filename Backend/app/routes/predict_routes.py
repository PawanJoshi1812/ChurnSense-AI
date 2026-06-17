from flask import Blueprint, request, jsonify
from app.services.prediction_service import predict_churn
from app.services.history_service import save_prediction

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # ✅ strict validation
        if not data or "features" not in data:
            return jsonify({
                "success": False,
                "error": "Request must contain 'features' array"
            }), 400

        features = data["features"]

        # ✅ extra safety check
        if not isinstance(features, list) or len(features) != 6:
            return jsonify({
                "success": False,
                "error": "Features must be a list of 6 numeric values"
            }), 400

        # 🔮 prediction
        result = predict_churn(features)

        # 💾 save history (safe)
        try:
            save_prediction(features, result)
        except Exception as history_error:
            print("History save failed:", history_error)

        return jsonify({
            "success": True,
            "prediction": result["prediction"],
            "prediction_label": result["prediction_label"],
            "churn_probability": round(float(result["churn_probability"]), 2)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500