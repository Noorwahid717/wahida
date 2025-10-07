from __future__ import annotations

from functools import lru_cache

from .chunking import MarkdownChunker
from .embeddings import EmbeddingModel
from .index import InMemoryVectorIndex
from .pipeline import RAGPipeline
from .reranker import KeywordReranker
from .runner import LocalCodeRunner


def create_pipeline() -> RAGPipeline:
    return RAGPipeline(
        chunker=MarkdownChunker(),
        embedder=EmbeddingModel(),
        index=InMemoryVectorIndex(),
        reranker=KeywordReranker(),
        code_runner=LocalCodeRunner(),
    )


@lru_cache(maxsize=1)
def get_pipeline() -> RAGPipeline:
    return create_pipeline()
