"""FastAPI entrypoint for Wahida backend."""

from __future__ import annotations

import json
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import RateLimiter, settings
from app.routers import chat, progress, quiz, run as run_router
from app.services.hint_policy import HintPolicy
from app.services.rag import RagService, ChunkPayload


@asynccontextmanager
def lifespan(app: FastAPI):
    moderation_blocklist = {"hack", "exploit", "porn", "radikal"}
    if settings.moderation_blocklist_path and Path(settings.moderation_blocklist_path).exists():
        moderation_blocklist = set(
            json.loads(Path(settings.moderation_blocklist_path).read_text(encoding="utf-8"))
        )
    app.state.moderation_blocklist = moderation_blocklist
    app.state.rate_limiters = {
        "chat": RateLimiter(settings.rate_limit_per_minute_chat, 60),
        "run": RateLimiter(settings.rate_limit_per_minute_run, 60),
    }
    app.state.hint_policy = HintPolicy()

    index_path = Path("data/faiss/index.bin")
    rag_service = RagService.load(index_path)
    if not rag_service.retrieve("tes"):
        seed_chunks = [
            ChunkPayload(
                chunk_id="seed-1",
                text="Belajar persamaan linear membutuhkan pemahaman bentuk ax + b = c.",
                metadata={"kelas": "X", "topik": "Persamaan Linear"},
            )
        ]
        rag_service.index(seed_chunks)
    app.state.rag_service = rag_service
    try:
        yield
    finally:
        index_path.parent.mkdir(parents=True, exist_ok=True)
        rag_service.dump(index_path)


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name, lifespan=lifespan)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/healthz")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    application.include_router(chat.router, prefix="/api")
    application.include_router(run_router.router, prefix="/api")
    application.include_router(quiz.router, prefix="/api")
    application.include_router(progress.router, prefix="/api")
    return application


app = create_app()


def run() -> None:  # pragma: no cover - manual entrypoint
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


__all__ = ["app", "create_app", "run"]
