
# --- Builder stage ---

FROM python:3.11-slim AS base

ENV POETRY_VERSION=1.8.3 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/poetry/bin:$PATH"

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python -

WORKDIR /app

# --- Builder stage ---
FROM base AS builder
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-interaction --no-root
COPY app ./app

# --- Runtime stage ---
FROM base AS runtime
RUN useradd --create-home --shell /bin/bash app && mkdir -p /app && chown -R app:app /app
WORKDIR /app
COPY --from=builder /app /app
USER app

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
