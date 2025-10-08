FROM python:3.11-slim AS base

ENV POETRY_VERSION=1.8.3 \ \
    POETRY_HOME=/opt/poetry \ \
    POETRY_VIRTUALENVS_CREATE=false \ \
    PYTHONUNBUFFERED=1 \ \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-interaction --no-root

COPY app ./app

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
