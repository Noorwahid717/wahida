from __future__ import annotations

import re
from typing import Iterable, List

from .types import SearchResult


WORD_PATTERN = re.compile(r"\w+")


class KeywordReranker:
    """Very lightweight lexical re-ranker."""

    def rerank(self, query: str, results: Iterable[SearchResult]) -> List[SearchResult]:
        query_terms = {term.lower() for term in WORD_PATTERN.findall(query)}
        scored: List[SearchResult] = []
        for result in results:
            chunk_terms = {term.lower() for term in WORD_PATTERN.findall(result.chunk.text)}
            overlap = len(query_terms & chunk_terms)
            score = result.score + (0.05 * overlap)
            scored.append(SearchResult(chunk=result.chunk, score=score))
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored
