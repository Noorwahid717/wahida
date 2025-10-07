from fastapi import APIRouter
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def create_chat_completion(payload: ChatRequest) -> ChatResponse:
    """Placeholder chat endpoint that will be replaced by RAG pipeline."""
    return ChatResponse(reply=f"Echo: {payload.message}")
