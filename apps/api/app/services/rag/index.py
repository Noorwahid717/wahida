from __future__ import annotations

from typing import Callable, Iterable, List, Optional

from .embeddings import _cosine_similarity
from .types import Filter, ModuleChunk, SearchResult, Vector


FilterFn = Callable[[ModuleChunk], bool]


class InMemoryVectorIndex:
    """Simple vector index storing embeddings in Python memory."""

    def __init__(self) -> None:
        self._vectors: List[Vector] = []
        self._chunks: List[ModuleChunk] = []

    def add(self, vectors: Iterable[Vector], chunks: Iterable[ModuleChunk]) -> None:
        for vector, chunk in zip(vectors, chunks):
            self._vectors.append(vector)
            self._chunks.append(chunk)

    def search(
        self,
        query_vector: Vector,
        top_k: int,
        filters: Optional[FilterFn] = None,
    ) -> List[SearchResult]:
        scores: List[SearchResult] = []
        for vector, chunk in zip(self._vectors, self._chunks):
            if filters and not filters(chunk):
                continue
            similarity = _cosine_similarity(query_vector, vector)
            scores.append(SearchResult(chunk=chunk, score=similarity))
        scores.sort(key=lambda result: result.score, reverse=True)
        return scores[:top_k]

    def __len__(self) -> int:
        return len(self._chunks)


def build_filter(filter_values: Filter) -> FilterFn:
    def _filter(chunk: ModuleChunk) -> bool:
        for key, value in filter_values.items():
            if value is None:
                continue
            if key == "collection":
                if chunk.metadata.get("collection") != value:
                    return False
            elif value and chunk.metadata.get(key) != value:
                return False
        return True

    return _filter
