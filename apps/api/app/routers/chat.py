from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..services.rag.container import get_pipeline
from ..services.rag.pipeline import RAGPipeline


class ChatRequest(BaseModel):
    message: str
    grade: Optional[str] = None
    topic: Optional[str] = None
    level: Optional[str] = None
    collection: Optional[str] = None
    top_k: int = 4


class ChatContext(BaseModel):
    chunk_id: str
    module_id: str
    topic: str
    level: str
    score: float
    text: str


class ChatResponse(BaseModel):
    reply: str
    contexts: list[ChatContext]
    exercises: list[str]
    code_feedback: Optional[str] = None
    generated_at: datetime


router = APIRouter(prefix="/chat", tags=["chat"])


def get_rag_pipeline() -> RAGPipeline:  # pragma: no cover - simple dependency shim
    return get_pipeline()


@router.post("/", response_model=ChatResponse)
async def create_chat_completion(
    payload: ChatRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline),
) -> ChatResponse:
    """RAG-driven chat completion with chunk retrieval and optional code execution."""

    filters = {
        "kelas": payload.grade,
        "topik": payload.topic,
        "level": payload.level,
        "collection": payload.collection,
    }
    rag_response = await pipeline.answer(payload.message, filters=filters, top_k=payload.top_k)
    contexts = [
        ChatContext(
            chunk_id=result.chunk.chunk_id,
            module_id=result.chunk.module_id,
            topic=result.chunk.metadata.get("topik", ""),
            level=result.chunk.metadata.get("level", ""),
            score=result.score,
            text=result.chunk.text,
        )
        for result in rag_response.contexts
    ]
    return ChatResponse(
        reply=rag_response.answer,
        contexts=contexts,
        exercises=rag_response.exercises,
        code_feedback=rag_response.code_feedback,
        generated_at=rag_response.generated_at,
    )
