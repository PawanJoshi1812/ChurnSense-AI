from flask import Blueprint, request, jsonify
from app.services.prediction_service import predict_churn
from app.services.history_service import save_prediction

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json["features"]

        result = predict_churn(data)

        # SAVE TO DATABASE
        save_prediction(data, result)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })