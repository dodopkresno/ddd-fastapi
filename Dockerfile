FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir "pip>=26.2,<27" \
    && pip wheel --no-cache-dir --wheel-dir /wheels "pip>=26.2,<27" .

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 APP_ENVIRONMENT=production
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels && useradd --uid 10001 --create-home app
USER 10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=3)"]
CMD ["uvicorn", "ddd_fastapi.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
