"""Celery tasks for Wahida API."""

from __future__ import annotations

from app.core import celery_app
from app.services.rag import RagService


@celery_app.task
def index_chunks(chunks: list[dict], index_path: str) -> None:
    """Index chunks into FAISS asynchronously."""
    service = RagService.load(index_path)
    payload_chunks = [RagService.ChunkPayload(**chunk) for chunk in chunks]
    service.index(payload_chunks)
    service.dump(index_path)