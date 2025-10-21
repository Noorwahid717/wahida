from __future__ import annotations

import asyncio
import json
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.core import RateLimitExceeded
from app.core.auth import get_current_user
from app.services.hint_policy import HintPolicy, HintState
from app.services.rag import RagService


class ModeratedChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


router = APIRouter(prefix="/chat", tags=["chat"])


def get_rag_service(request: Request) -> RagService:
    service: RagService | None = getattr(request.app.state, "rag_service", None)
    if not service:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "RAG service not initialised")
    return service


def enforce_chat_rate_limit(request: Request) -> None:
    limiter = request.app.state.rate_limiters["chat"]
    client_host = request.client.host if request.client else "anonymous"
    try:
        limiter.hit(client_host)
    except RateLimitExceeded as exc:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, str(exc)) from exc


async def moderation_guard(request: Request, payload: ModeratedChatRequest) -> None:
    if any(bad_word in payload.message.lower() for bad_word in request.app.state.moderation_blocklist):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Pesan melanggar kebijakan moderasi.")


async def _generate_events(
    request: Request,
    rag_service: RagService,
    payload: ModeratedChatRequest,
    hint_policy: HintPolicy,
) -> AsyncGenerator[str, None]:
    retrieved = rag_service.retrieve(payload.message, top_k=3)
    state = HintState()
    yield "event: status\n" "data: {\"type\": \"started\"}\n\n"
    for chunk in retrieved:
        if await request.is_disconnected():
            break
        state = hint_policy.evaluate(payload.message, state)
        chunk_payload = {
            "type": "chunk",
            "text": chunk.text,
            "metadata": chunk.metadata,
            "score": chunk.score,
            "hintsRevealed": state.hints_revealed,
        }
        yield f"data: {json.dumps(chunk_payload, ensure_ascii=False)}\n\n"
        await asyncio.sleep(0.05)

    # Generate adaptive response using LLM
    llm_response = await rag_service.generate_response(payload.message, retrieved)
    yield f"data: {json.dumps({'type': 'response', 'text': llm_response}, ensure_ascii=False)}\n\n"

    yield "event: status\n" "data: {\"type\": \"completed\"}\n\n"


@router.post(
    "/",
    response_class=StreamingResponse,
    dependencies=[Depends(get_current_user)],
)
async def create_chat_completion(
    payload: ModeratedChatRequest,
    request: Request,
    _: None = Depends(enforce_chat_rate_limit),
    rag_service: RagService = Depends(get_rag_service),
) -> StreamingResponse:
    """Stream chunks retrieved from the RAG index via SSE."""

    await moderation_guard(request, payload)
    hint_policy: HintPolicy = request.app.state.hint_policy
    generator = _generate_events(request, rag_service, payload, hint_policy)
    return StreamingResponse(generator, media_type="text/event-stream")
