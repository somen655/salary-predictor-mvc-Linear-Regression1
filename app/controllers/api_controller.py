from flask import Blueprint, jsonify, request, current_app
from ..models.schemas import PredictRequestSchema
from ..models.regression import ModelRegistry
from ..services.metrics import evaluate_from_csv

api_bp = Blueprint("api", __name__)

@api_bp.get("/health")
def health():
    return jsonify(status="ok", model_loaded=ModelRegistry.is_loaded(), version=current_app.config.get("MODEL_VERSION", "unknown"))

@api_bp.post("/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    data, errors = PredictRequestSchema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    model = ModelRegistry.get()
    yhat = model.predict_one(data)

    return jsonify({
        "predicted_salary_inr": int(yhat),
        "currency": "INR",
        "model_version": current_app.config.get("MODEL_VERSION", "unknown")
    })

@api_bp.post("/train")
def train():
    # retrain from data/salary_data.csv
    metrics = evaluate_from_csv()
    # hot-reload model
    ModelRegistry.load(force=True)
    return jsonify(metrics), 200
