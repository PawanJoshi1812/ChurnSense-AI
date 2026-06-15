from flask import Blueprint, jsonify
from app.models.prediction_history import PredictionHistory

history_bp = Blueprint("history", __name__)

@history_bp.route("/history", methods=["GET"])
def get_history():
    try:
        records = PredictionHistory.query.order_by(PredictionHistory.created_at.desc()).all()

        data = []

        for r in records:
            data.append({
                "id": r.id,
                "customer_data": r.customer_data,
                "prediction": r.prediction,
                "probability": r.probability,
                "created_at": r.created_at
            })

        return jsonify({
            "success": True,
            "data": data
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })