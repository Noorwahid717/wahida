from __future__ import annotations

import re
from typing import Iterable, List

from .types import ModuleChunk, ModuleDocument


HEADING_PATTERN = re.compile(r"^#+ ", re.MULTILINE)


class MarkdownChunker:
    """Chunk markdown documents by headings/paragraphs with ~500 token target."""

    def __init__(self, target_tokens: int = 500) -> None:
        self.target_tokens = target_tokens

    def chunk(self, document: ModuleDocument) -> List[ModuleChunk]:
        raw_sections = self._split_by_heading(document.markdown)
        chunks: List[ModuleChunk] = []
        order = 0
        for section in raw_sections:
            paragraphs = [p.strip() for p in section.split("\n\n") if p.strip()]
            buffer: List[str] = []
            buffer_tokens = 0
            for paragraph in paragraphs:
                paragraph_tokens = self._estimate_tokens(paragraph)
                if buffer_tokens + paragraph_tokens > self.target_tokens and buffer:
                    chunks.append(self._create_chunk(document, order, buffer))
                    order += 1
                    buffer = []
                    buffer_tokens = 0
                buffer.append(paragraph)
                buffer_tokens += paragraph_tokens
            if buffer:
                chunks.append(self._create_chunk(document, order, buffer))
                order += 1
        return chunks

    def _split_by_heading(self, markdown: str) -> Iterable[str]:
        if not markdown.strip():
            return []
        sections = HEADING_PATTERN.split(markdown)
        headings = HEADING_PATTERN.findall(markdown)
        combined: List[str] = []
        for idx, section in enumerate(sections):
            title = headings[idx - 1] if idx > 0 else ""
            combined.append(f"{title}{section}".strip())
        return [section for section in combined if section]

    def _estimate_tokens(self, text: str) -> int:
        # Rough approximation: assume 1 token ~= 0.75 words.
        words = len(re.findall(r"\w+", text))
        return max(1, int(words / 0.75))

    def _create_chunk(self, document: ModuleDocument, order: int, paragraphs: List[str]) -> ModuleChunk:
        chunk_text = "\n\n".join(paragraphs)
        tokens = self._estimate_tokens(chunk_text)
        metadata = {
            "kelas": document.grade,
            "topik": document.topic,
            "level": document.level,
            "collection": document.collection,
            **document.metadata,
        }
        chunk_id = f"{document.module_id}:{order}"
        return ModuleChunk(
            chunk_id=chunk_id,
            module_id=document.module_id,
            order=order,
            text=chunk_text,
            tokens=tokens,
            metadata=metadata,
        )
