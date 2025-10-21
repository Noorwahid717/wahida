"""Minimal RAG service powering chat retrieval."""

from __future__ import annotations

import hashlib
import httpx
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import faiss
import numpy as np
from openai import OpenAI

from app.core.config import settings


@dataclass(slots=True)
class RetrievedChunk:
    """Chunk payload returned from the retriever."""

    chunk_id: str
    text: str
    metadata: dict[str, str]
    score: float


@dataclass(slots=True)
class ChunkPayload:
    """Serializable representation of a chunk to index."""

    chunk_id: str
    text: str
    metadata: dict[str, str]


class RagService:
    """Simple FAISS-backed retriever with a hookable re-ranker."""

    def __init__(self, dimension: int = 384) -> None:
        self.dimension = dimension
        self._index = faiss.IndexFlatIP(self.dimension)
        self._chunks: list[ChunkPayload] = []

    @staticmethod
    def _embed(text: str, dimension: int) -> np.ndarray:
        if settings.openai_api_key:
            client = OpenAI(api_key=settings.openai_api_key)
            response = client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            return np.array(response.data[0].embedding, dtype="float32")
        else:
            # Fallback to dummy hash
            tokens = text.lower().split()
            vector = np.zeros(dimension, dtype="float32")
            for token in tokens:
                token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
                index = int(token_hash[:8], 16) % dimension
                vector[index] += 1
            return vector / np.linalg.norm(vector) if np.linalg.norm(vector) > 0 else vector

    def index(self, payloads: Iterable[ChunkPayload]) -> None:
        """Add chunks to the FAISS index."""

        vectors = []
        for payload in payloads:
            embedding = self._embed(payload.text, self.dimension)
            vectors.append(embedding)
            self._chunks.append(payload)
        if vectors:
            stacked = np.vstack(vectors)
            self._index.add(stacked)

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        if not self._chunks:
            return []
        query_vec = self._embed(query, self.dimension)[np.newaxis, :]
        scores, indices = self._index.search(query_vec, min(top_k, len(self._chunks)))
        results: list[RetrievedChunk] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            payload = self._chunks[idx]
            results.append(
                RetrievedChunk(
                    chunk_id=payload.chunk_id,
                    text=payload.text,
                    metadata=payload.metadata,
                    score=float(score),
                )
            )
        return self.re_rank(query, results)

    def re_rank(self, query: str, chunks: Sequence[RetrievedChunk]) -> list[RetrievedChunk]:
        """Simple re-ranking hook using cosine similarity fallback."""

        if not chunks:
            return []
        query_vec = self._embed(query, self.dimension)
        scored = []
        for chunk in chunks:
            chunk_vec = self._embed(chunk.text, self.dimension)
            rerank_score = float(np.dot(query_vec, chunk_vec))
            scored.append((rerank_score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored]

    def dump(self, path: Path) -> None:
        """Persist the in-memory index and payloads."""

        path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self._index, str(path))
        payload_path = path.with_suffix(".json")
        payload_path.write_text(
            json.dumps([chunk.__dict__ for chunk in self._chunks], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: Path) -> "RagService":
        service = cls()
        if path.exists():
            service._index = faiss.read_index(str(path))
            payload_file = path.with_suffix(".json")
            if payload_file.exists():
                payloads = json.loads(payload_file.read_text(encoding="utf-8"))
                service._chunks = [ChunkPayload(**payload) for payload in payloads]
        return service

    async def generate_response(self, query: str, retrieved_chunks: list[RetrievedChunk]) -> str:
        """Generate adaptive response using Google Gemini API directly."""
        if not settings.google_gemini_api_key:
            return "LLM not configured. Retrieved chunks: " + "; ".join([c.text for c in retrieved_chunks])

        try:
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={settings.google_gemini_api_key}"
            system_prompt = """Anda adalah Tutor Informatika untuk siswa SMA.
Tugas: jelaskan konsep dengan bahasa sederhana, gunakan analogi keseharian,
berikan contoh kode Python kecil, dan latihan 5–10 menit.
Jangan selesaikan PR penuh; aktifkan "hint policy".
Tunjukkan langkah berpikir, sebutkan kesalahan umum, dan tutup dengan refleksi.
Jika topik di luar konteks, katakan tidak yakin dan sarankan eksperimen aman.
Di akhir respons: berikan 1–2 latihan dan 1 pertanyaan refleksi."""

            context = "\n".join([f"- {chunk.text} (metadata: {chunk.metadata})" for chunk in retrieved_chunks])
            prompt = f"{system_prompt}\n\nBased on the following context, answer the query adaptively:\n\nContext:\n{context}\n\nQuery: {query}\n\nProvide a helpful, educational response."

            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()

            if "candidates" in data and data["candidates"]:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return f"No response from Gemini. Retrieved chunks: " + "; ".join([c.text for c in retrieved_chunks])

        except Exception as e:
            return f"Error calling Gemini API: {str(e)}. Retrieved chunks: " + "; ".join([c.text for c in retrieved_chunks])


# Celery task
from app.celery_app import celery_app

@celery_app.task
def embed_text(text: str) -> list[float]:
    """Embed text using OpenAI."""
    if not settings.openai_api_key:
        raise ValueError("OpenAI API key not configured")
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


__all__ = ["ChunkPayload", "RetrievedChunk", "RagService"]
