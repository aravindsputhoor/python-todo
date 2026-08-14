# ==============================
# Stage 1 - Builder
# ==============================

FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir \
    --prefix=/install \
    -r requirements.txt


# ==============================
# Stage 2 - Production
# ==============================

FROM python:3.12-slim

WORKDIR /app

# Copy installed Python packages
COPY --from=builder /install /usr/local

# Copy application
COPY app ./app
COPY run.py .

# Create non-root user
RUN useradd \
    --create-home \
    --shell /bin/bash \
    appuser

# Change ownership
RUN chown -R appuser:appuser /app

# Use non-root user
USER appuser

EXPOSE 5000

# Container health check
HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=10s \
    --retries=3 \
    CMD python -c \
    "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]