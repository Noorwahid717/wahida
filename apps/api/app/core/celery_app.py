"""Celery configuration."""

from __future__ import annotations

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "wahida",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks"],
)