from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


DEFAULT_MODEL_PATH = Path(__file__).resolve().parent / "model.joblib"


def train_and_save_model(model_path=DEFAULT_MODEL_PATH):
    rng = np.random.default_rng(42)
    sample_count = 5000
    annual_income = rng.uniform(15_000, 250_000, size=sample_count)
    loan_amount = rng.uniform(1_000, 100_000, size=sample_count)
    credit_score = rng.uniform(300, 850, size=sample_count)
    employment_years = rng.uniform(0, 40, size=sample_count)
    debt_to_income = rng.uniform(0, 1, size=sample_count)

    features = np.column_stack((
        annual_income,
        loan_amount,
        credit_score,
        employment_years,
        debt_to_income,
    ))
    score = (
        (credit_score - 650) / 45
        + (annual_income - 60_000) / 30_000
        - (loan_amount - 20_000) / 15_000
        + (employment_years - 5) * 0.05
        - (debt_to_income - 0.35) * 5
    )
    approval_probability = 1 / (1 + np.exp(-score))
    labels = rng.binomial(1, approval_probability)

    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(random_state=42, max_iter=1000),
    )
    model.fit(features, labels)

    output_path = Path(model_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    return output_path


if __name__ == "__main__":
    saved_path = train_and_save_model()
    print(f"Trained model saved to: {saved_path}")
