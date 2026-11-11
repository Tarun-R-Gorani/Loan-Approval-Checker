import math
import os
from pathlib import Path

import joblib
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest


MODEL_PATH = Path(__file__).resolve().parent / "model.joblib"
FEATURE_RANGES = {
    "annual_income": (0, 1_000_000),
    "loan_amount": (1, 500_000),
    "credit_score": (300, 850),
    "employment_years": (0, 60),
    "debt_to_income": (0, 1),
}
FEATURES = tuple(FEATURE_RANGES)


def create_app(model_path=MODEL_PATH):
    model_file = Path(model_path)
    if not model_file.is_file():
        raise FileNotFoundError(
            f"Model not found at {model_file}. Run 'python train_model.py' first."
        )

    model = joblib.load(model_file)
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/predict")
    def predict():
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json."}), 415

        try:
            payload = request.get_json()
        except BadRequest:
            return jsonify({"error": "Request body must contain valid JSON."}), 400

        if not isinstance(payload, dict) or set(payload) != {"features"}:
            return jsonify({
                "error": "Request JSON must contain only a 'features' object."
            }), 400

        features = payload["features"]
        if not isinstance(features, dict):
            return jsonify({"error": "'features' must be a JSON object."}), 400

        missing = [name for name in FEATURES if name not in features]
        unexpected = [name for name in features if name not in FEATURES]
        if missing or unexpected:
            return jsonify({
                "error": "Feature names do not match the model.",
                "missing": missing,
                "unexpected": unexpected,
                "expected": list(FEATURES),
            }), 400

        values = []
        for name in FEATURES:
            value = features[name]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return jsonify({"error": f"'{name}' must be a number."}), 400
            try:
                numeric_value = float(value)
            except OverflowError:
                return jsonify({"error": f"'{name}' must be finite."}), 400
            if not math.isfinite(numeric_value):
                return jsonify({"error": f"'{name}' must be finite."}), 400
            values.append(numeric_value)

        for name, value in zip(FEATURES, values):
            minimum, maximum = FEATURE_RANGES[name]
            if not minimum <= value <= maximum:
                return jsonify({
                    "error": f"'{name}' must be between {minimum} and {maximum}."
                }), 400

        approved = bool(model.predict([values])[0])
        probability = float(model.predict_proba([values])[0][1])
        return jsonify({
            "decision": "demo_approved" if approved else "demo_not_approved",
            "approval_probability": probability,
            "disclaimer": (
                "Illustrative demo only; this synthetic model must not be used "
                "to make real lending or credit decisions."
            ),
        })

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_HOST", "127.0.0.1"),
        port=int(os.environ.get("FLASK_PORT", "5000")),
        debug=False,
    )
