"""Ingest markdown content into FAISS and optionally pgvector."""

from __future__ import annotations

import argparse
import json
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

from app.services.rag import ChunkPayload, RagService

try:  # optional dependency, only used when DSN provided
    import psycopg
except ImportError:  # pragma: no cover - optional
    psycopg = None  # type: ignore


@dataclass(slots=True)
class MarkdownDocument:
    path: Path
    metadata: dict[str, str]
    body: str


# rest of file remains? need to append? We'll re-add existing content below.

def load_markdown_documents(content_dir: Path) -> list[MarkdownDocument]:
    documents: list[MarkdownDocument] = []
    for path in content_dir.rglob("*.md"):
        raw = path.read_text(encoding="utf-8")
        if raw.startswith("---"):
            _, front_matter, body = raw.split("---", 2)
            metadata = yaml.safe_load(front_matter) or {}
            documents.append(MarkdownDocument(path=path, metadata=metadata, body=body.strip()))
    return documents


def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    words = text.split()
    if not words:
        return []
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk_words = words[i : i + chunk_size]
        chunks.append(" ".join(chunk_words))
    return chunks


def upsert_pgvector(dsn: str, payloads: Iterable[ChunkPayload]) -> None:
    if not psycopg:
        raise RuntimeError("psycopg is required for Postgres ingestion")
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            for payload in payloads:
                cur.execute(
                    textwrap.dedent(
                        """
                        INSERT INTO chunks (id, content_id, ord, text, tokens, metadata)
                        VALUES (%(chunk_id)s, %(content_id)s, %(ord)s, %(text)s, %(tokens)s, %(metadata)s)
                        ON CONFLICT (id) DO UPDATE SET text = EXCLUDED.text
                        """
                    ),
                    {
                        "chunk_id": payload.chunk_id,
                        "content_id": payload.metadata.get("content_id", payload.chunk_id),
                        "ord": int(payload.metadata.get("ord", 0)),
                        "text": payload.text,
                        "tokens": len(payload.text.split()),
                        "metadata": json.dumps(payload.metadata),
                    },
                )
        conn.commit()


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest markdown content into FAISS index")
    parser.add_argument("--content-dir", type=Path, default=Path("content"), help="Directory with markdown files")
    parser.add_argument("--faiss-path", type=Path, default=Path("data/faiss/index.bin"))
    parser.add_argument("--postgres-dsn", type=str, default=None)
    args = parser.parse_args()

    documents = load_markdown_documents(args.content_dir)
    rag = RagService()
    chunk_payloads: list[ChunkPayload] = []
    for doc in documents:
        doc_id = doc.metadata.get("id", doc.path.stem)
        for idx, chunk in enumerate(chunk_text(doc.body)):
            chunk_payloads.append(
                ChunkPayload(
                    chunk_id=f"{doc_id}-{idx}",
                    text=chunk,
                    metadata={
                        "kelas": doc.metadata.get("kelas", ""),
                        "topik": doc.metadata.get("topik", ""),
                        "level": doc.metadata.get("level", ""),
                        "tags": ",".join(doc.metadata.get("tags", [])),
                        "content_id": doc_id,
                        "ord": str(idx),
                    },
                )
            )
    rag.index(chunk_payloads)
    args.faiss_path.parent.mkdir(parents=True, exist_ok=True)
    rag.dump(args.faiss_path)

    if args.postgres_dsn:
        upsert_pgvector(args.postgres_dsn, chunk_payloads)


if __name__ == "__main__":  # pragma: no cover - script entrypoint
    main()
