import tempfile
import unittest
from pathlib import Path

from app import FEATURES, create_app
from train_model import train_and_save_model


class PredictionApiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        model_path = Path(self.temp_dir.name) / "model.joblib"
        train_and_save_model(model_path)
        self.client = create_app(model_path).test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_health(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_prediction(self):
        features = {
            "annual_income": 75000,
            "loan_amount": 20000,
            "credit_score": 720,
            "employment_years": 8,
            "debt_to_income": 0.25,
        }
        response = self.client.post("/predict", json={"features": features})

        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertIn(result["decision"], {"demo_approved", "demo_not_approved"})
        self.assertGreaterEqual(result["approval_probability"], 0)
        self.assertLessEqual(result["approval_probability"], 1)
        self.assertIn("must not be used", result["disclaimer"])

    def test_rejects_missing_feature(self):
        response = self.client.post(
            "/predict",
            json={"features": {"annual_income": 75000, "loan_amount": 20000}},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("credit_score", response.get_json()["missing"])

    def test_rejects_non_numeric_feature(self):
        features = dict.fromkeys(FEATURES, 1)
        features["credit_score"] = "high"
        response = self.client.post("/predict", json={"features": features})

        self.assertEqual(response.status_code, 400)
        self.assertIn("must be a number", response.get_json()["error"])

    def test_rejects_non_json_request(self):
        response = self.client.post("/predict", data="not json")

        self.assertEqual(response.status_code, 415)
        self.assertIn("application/json", response.get_json()["error"])

    def test_rejects_malformed_json(self):
        response = self.client.post(
            "/predict",
            data="{",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("valid JSON", response.get_json()["error"])

    def test_rejects_number_outside_float_range(self):
        features = dict.fromkeys(FEATURES, 1)
        features["annual_income"] = 10**400
        response = self.client.post("/predict", json={"features": features})

        self.assertEqual(response.status_code, 400)
        self.assertIn("must be finite", response.get_json()["error"])

    def test_rejects_out_of_range_feature(self):
        features = {
            "annual_income": 75000,
            "loan_amount": 20000,
            "credit_score": 900,
            "employment_years": 8,
            "debt_to_income": 0.25,
        }
        response = self.client.post("/predict", json={"features": features})

        self.assertEqual(response.status_code, 400)
        self.assertIn("between 300 and 850", response.get_json()["error"])


if __name__ == "__main__":
    unittest.main()
