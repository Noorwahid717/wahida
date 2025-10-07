from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Sequence


@dataclass
class ModuleDocument:
    """Represents a learning module markdown document."""

    module_id: str
    title: str
    grade: str
    topic: str
    level: str
    markdown: str
    collection: str = "default"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModuleChunk:
    """Represents a chunk of a module ready for embedding."""

    chunk_id: str
    module_id: str
    order: int
    text: str
    tokens: int
    metadata: Dict[str, Any]


@dataclass
class SearchResult:
    chunk: ModuleChunk
    score: float


@dataclass
class RAGResponse:
    answer: str
    contexts: List[SearchResult]
    exercises: List[str]
    code_feedback: str | None = None
    generated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class CodeBlock:
    language: str
    source: str
    origin_chunk: ModuleChunk


Filter = Dict[str, Any]
Vector = Sequence[float]
Vectors = Iterable[Vector]
