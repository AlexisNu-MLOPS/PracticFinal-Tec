# Multi-stage Dockerfile for Titanic ML Project
# Stage 1: Base image with shared dependencies
FROM python:3.10-slim as base

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────────────────
# Stage 2: Processing image (SageMaker Processing Job)
#   - Reads  : /opt/ml/processing/input/raw/
#   - Writes : /opt/ml/processing/output/
#   - SageMaker syncs output → S3 automatically
# ─────────────────────────────────────────────────────────
FROM base as processing

COPY src/ ./src/
COPY scripts/ ./scripts/

# SageMaker mounts data at runtime; directories must exist
RUN mkdir -p /opt/ml/processing/input/raw \
    /opt/ml/processing/output

ENTRYPOINT ["python", "/app/src/process.py"]

# ─────────────────────────────────────────────────────────
# Stage 3: Training image (SageMaker Training Job)
#   - Reads  : /opt/ml/input/data/train/
#   - Writes : /opt/ml/model/
# ─────────────────────────────────────────────────────────
FROM base as train

COPY src/ ./src/
COPY scripts/ ./scripts/

RUN mkdir -p /opt/ml/input/data \
    /opt/ml/model \
    reports

ENTRYPOINT ["python", "/app/src/train.py"]

# ─────────────────────────────────────────────────────────
# Stage 4: Development image (local use / CI)
# ─────────────────────────────────────────────────────────
FROM base as development

COPY . .

RUN mkdir -p data/raw data/processed models reports
RUN python scripts/download_data.py

CMD ["bash"]

# ─────────────────────────────────────────────────────────
# Stage 5: Production image (lightweight inference)
# ─────────────────────────────────────────────────────────
FROM python:3.10-slim as production

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY scripts/ ./scripts/
COPY --from=development /app/models/ ./models/
COPY --from=development /app/data/ ./data/

RUN useradd -m -u 1000 mluser && \
    chown -R mluser:mluser /app

USER mluser

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

CMD ["python", "src/evaluate.py", "--model", "models/titanic_model_random_forest.pkl", "--use-test"]
