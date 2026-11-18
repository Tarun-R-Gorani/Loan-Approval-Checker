# Loan Approval Demo API

A Flask REST API with a reproducibly trained, synthetic loan-approval
classifier. This is a learning/demo project only: do not use its decisions or
probabilities for real lending, credit eligibility, or other consequential
decisions. Its synthetic data and probabilities are not representative or
validated for real applicants.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python train_model.py
```

## Run the application

### Docker Compose (portable deployment)

Install and start Docker Desktop, then from the project directory run:

```powershell
docker compose up --build
```

Compose builds the image, trains the synthetic demo model during image
creation, waits for the Flask health check, and starts both services. Open
`http://localhost:8501` for the Streamlit UI. The API is also available at
`http://localhost:5000` for Postman (`GET /health`, `POST /predict`).

Stop the services with **Ctrl+C**, then remove the containers with:

```powershell
docker compose down
```

To run in the background, use `docker compose up --build -d`; view logs with
`docker compose logs -f` and stop with `docker compose down`. The model is
baked into the image and regenerated on rebuild; no local Python virtual
environment is needed for Docker deployment.

### Run locally without Docker

Start the Flask API in one terminal:

```powershell
python app.py
```

In a second terminal, activate the same virtual environment and start the UI:

```powershell
cd "C:\Users\AIML-LAB1-34\Desktop\MLOps ML prediction Using Flask API"
.\.venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
```

Streamlit opens at `http://localhost:8501`. The API listens at
`http://127.0.0.1:5000`; enter a different API base URL in the UI sidebar if
your Flask service uses another address.

The UI includes an API health check, validated applicant inputs, and a
prediction panel that displays the response from Flask.

## Endpoints

### Health check

`GET /health`

```json
{"status": "ok"}
```

### Loan approval demo

`POST /predict` with `Content-Type: application/json`

```json
{
  "features": {
    "annual_income": 75000,
    "loan_amount": 20000,
    "credit_score": 720,
    "employment_years": 8,
    "debt_to_income": 0.25
  }
}
```

Features: annual income (0–1,000,000), loan amount (1–500,000), credit score
(300–850), employment years (0–60), and debt-to-income ratio (0–1).

Example API response:

```json
{
  "decision": "demo_approved",
  "approval_probability": 0.82,
  "disclaimer": "Illustrative demo only; this synthetic model must not be used to make real lending or credit decisions."
}
```

In Postman, choose **POST**, enter `http://127.0.0.1:5000/predict`, select
**Body → raw → JSON**, and send the example request. A malformed request or
feature mismatch or out-of-range value returns HTTP 400 with a JSON error.
After retraining, restart `python app.py` so the running service loads the new
model artifact. The Streamlit UI sends requests to Flask; it does not load or
run the model itself.

## Tests

```powershell
python -m unittest discover -s tests
```

## CI/CD and Docker Hub

GitHub Actions runs unit tests and builds the Docker image for pushes to `main`,
pull requests targeting `main`, and manual workflow runs. Successful pushes to
`main` and manual runs publish the image to Docker Hub:

```text
tarungorani/loan-approval-checker:latest
tarungorani/loan-approval-checker:sha-<commit>
```

Configure this repository secret before the first push or manual publish:

- `DOCKERHUB_TOKEN`: a Docker Hub personal access token with read/write access

Create the token in Docker Hub under **Account Settings → Personal access
tokens**. In GitHub, add it under **Settings → Secrets and variables →
Actions → New repository secret**. Pull requests build and test the image but
do not push it to Docker Hub.
