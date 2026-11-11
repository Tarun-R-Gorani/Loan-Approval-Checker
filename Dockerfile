FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt \
    && groupadd --system app \
    && useradd --system --gid app --create-home app

COPY --chown=app:app app.py streamlit_app.py train_model.py ./

RUN python train_model.py \
    && chown app:app model.joblib

USER app

EXPOSE 5000 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
