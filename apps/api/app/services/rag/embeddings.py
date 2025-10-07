from __future__ import annotations

import hashlib
import math
from typing import Iterable, List

from .types import Vector


class EmbeddingModel:
    """Simple deterministic embedding model placeholder."""

    def __init__(self, dimension: int = 256) -> None:
        self.dimension = dimension

    async def embed(self, texts: Iterable[str]) -> List[Vector]:
        return [self._embed_text(text) for text in texts]

    def _embed_text(self, text: str) -> Vector:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        repeated = (digest * ((self.dimension // len(digest)) + 1))[: self.dimension]
        vector = [float(byte) for byte in repeated]
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [value / norm for value in vector]


async def cosine_similarity(vector_a: Vector, vector_b: Vector) -> float:
    return _cosine_similarity(vector_a, vector_b)


def _cosine_similarity(vector_a: Vector, vector_b: Vector) -> float:
    dot = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
