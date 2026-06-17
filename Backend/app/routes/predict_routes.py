from flask import Blueprint, request, jsonify
from app.services.prediction_service import predict_churn
from app.services.history_service import save_prediction

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        # ✅ safer JSON parsing for production (Render fixes)
        data = request.get_json(silent=True) or {}

        features = data.get("features", None)

        # 🔴 FIX 1: handle missing input safely
        if features is None:
            return jsonify({
                "success": False,
                "prediction": 0,
                "prediction_label": "Invalid Input",
                "churn_probability": 0,
                "error": "Missing 'features' key"
            }), 200

        # 🔴 FIX 2: type safety
        if not isinstance(features, list):
            return jsonify({
                "success": False,
                "prediction": 0,
                "prediction_label": "Invalid Input",
                "churn_probability": 0,
                "error": "Features must be a list"
            }), 200

        # 🔴 FIX 3: length safety
        if len(features) != 6:
            return jsonify({
                "success": False,
                "prediction": 0,
                "prediction_label": "Invalid Input",
                "churn_probability": 0,
                "error": f"Expected 6 features, got {len(features)}"
            }), 200

        # 🔮 prediction
        result = predict_churn(features)

        # 💾 save history (safe, non-blocking)
        try:
            save_prediction(features, result)
        except Exception as history_error:
            print("History save failed:", history_error)

        return jsonify({
            "success": True,
            "prediction": result["prediction"],
            "prediction_label": result["prediction_label"],
            "churn_probability": round(float(result["churn_probability"]), 2)
        }), 200

    except Exception as e:
        print("ERROR:", str(e))

        return jsonify({
            "success": False,
            "prediction": 0,
            "prediction_label": "Server Error",
            "churn_probability": 0,
            "error": str(e)
        }), 200