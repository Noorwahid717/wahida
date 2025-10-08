"""Tests for the FAISS-backed retriever."""

from app.services.rag import ChunkPayload, RagService


def test_retriever_returns_relevant_chunks() -> None:
    service = RagService()
    service.index(
        [
            ChunkPayload(chunk_id="1", text="Persamaan linear sederhana", metadata={"topik": "aljabar"}),
            ChunkPayload(chunk_id="2", text="Fotosintesis tanaman", metadata={"topik": "biologi"}),
            ChunkPayload(chunk_id="3", text="Perang Diponegoro sejarah", metadata={"topik": "sejarah"}),
        ]
    )

    results = service.retrieve("bagaimana menyelesaikan persamaan linear", top_k=2)
    assert results
    assert results[0].chunk_id == "1"
    assert results[0].metadata["topik"] == "aljabar"
