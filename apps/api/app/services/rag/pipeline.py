from __future__ import annotations

import asyncio
import re
from typing import Iterable, List, Optional

from .chunking import MarkdownChunker
from .embeddings import EmbeddingModel
from .index import InMemoryVectorIndex, build_filter
from .reranker import KeywordReranker
from .runner import LocalCodeRunner, RunnerLike
from .types import CodeBlock, Filter, ModuleDocument, RAGResponse, SearchResult

CODE_BLOCK_PATTERN = re.compile(r"```(\w+)?\n([\s\S]*?)```", re.MULTILINE)


class RAGPipeline:
    def __init__(
        self,
        *,
        chunker: MarkdownChunker,
        embedder: EmbeddingModel,
        index: InMemoryVectorIndex,
        reranker: KeywordReranker | None = None,
        code_runner: RunnerLike = None,
    ) -> None:
        self.chunker = chunker
        self.embedder = embedder
        self.index = index
        self.reranker = reranker
        self.code_runner = code_runner or LocalCodeRunner()

    async def ingest_module(self, document: ModuleDocument) -> None:
        chunks = self.chunker.chunk(document)
        vectors = await self.embedder.embed(chunk.text for chunk in chunks)
        self.index.add(vectors, chunks)

    async def answer(
        self,
        query: str,
        *,
        filters: Optional[Filter] = None,
        top_k: int = 4,
    ) -> RAGResponse:
        filters = filters or {}
        query_vector = (await self.embedder.embed([query]))[0]
        filter_fn = build_filter(filters)
        retrieved = self.index.search(query_vector, top_k, filters=filter_fn)
        if self.reranker:
            retrieved = self.reranker.rerank(query, retrieved)
        answer = self._compose_answer(query, retrieved)
        exercises = self._generate_exercises(retrieved)
        code_feedback = await self._maybe_run_code(retrieved)
        return RAGResponse(
            answer=answer,
            contexts=retrieved,
            exercises=exercises,
            code_feedback=code_feedback,
        )

    def _compose_answer(self, query: str, results: Iterable[SearchResult]) -> str:
        if not results:
            return "Maaf, aku belum menemukan materi terkait. Silakan jelaskan lagi pertanyaannya."
        highlights = []
        for result in results:
            snippet = result.chunk.text.strip().split("\n\n")[0]
            highlights.append(f"- {snippet[:240]}...")
        joined = "\n".join(highlights)
        return (
            "Berikut ringkasan materi yang relevan dengan pertanyaanmu:\n"
            f"{joined}\n\n"
            "Aku juga menambahkan latihan yang bisa kamu coba untuk memperdalam pemahaman."
        )

    def _generate_exercises(self, results: Iterable[SearchResult]) -> List[str]:
        exercises: List[str] = []
        for result in results:
            topic = result.chunk.metadata.get("topik", "materi")
            level = result.chunk.metadata.get("level", "dasar")
            exercises.append(
                (
                    f"Latihan {topic} ({level}): jelaskan kembali inti materi dan buat satu contoh soal."
                )
            )
        return exercises[:2]

    async def _maybe_run_code(self, results: Iterable[SearchResult]) -> str | None:
        code_blocks = list(self._extract_code_blocks(results))
        if not code_blocks or not self.code_runner:
            return None
        # Run only the first snippet to keep feedback quick in MVP.
        block = code_blocks[0]
        response = await self.code_runner.run(language=block.language or "python", source=block.source)
        if response.stderr:
            return f"Kode menghasilkan error: {response.stderr}"
        return f"Hasil eksekusi kode: {response.stdout} (status: {response.status})"

    def _extract_code_blocks(self, results: Iterable[SearchResult]) -> Iterable[CodeBlock]:
        for result in results:
            for match in CODE_BLOCK_PATTERN.finditer(result.chunk.text):
                language = (match.group(1) or "python").strip()
                source = match.group(2).strip()
                yield CodeBlock(language=language, source=source, origin_chunk=result.chunk)


async def ingest_bulk(pipeline: RAGPipeline, modules: Iterable[ModuleDocument]) -> None:
    await asyncio.gather(*(pipeline.ingest_module(module) for module in modules))
