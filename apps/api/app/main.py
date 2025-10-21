"""FastAPI entrypoint for Wahida backend."""

from __future__ import annotations

import json
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
env_file_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_file_path)

from app.core import RateLimiter, settings
# from app.core import RateLimiter, settings, Base, SessionLocal, get_db
from app.routers import chat, progress, quiz, run as run_router
from app.services.hint_policy import HintPolicy
from app.services.rag import RagService, ChunkPayload

def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name)  # Removed lifespan for debugging
    # FastAPIInstrumentor.instrument_app(application)  # Commented out for debugging
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Manual setup since lifespan removed
    moderation_blocklist = {"hack", "exploit", "porn", "radikal"}
    if settings.moderation_blocklist_path and settings.moderation_blocklist_path.strip() and Path(settings.moderation_blocklist_path).exists():
        moderation_blocklist = set(
            json.loads(Path(settings.moderation_blocklist_path).read_text(encoding="utf-8"))
        )
    application.state.moderation_blocklist = moderation_blocklist
    application.state.rate_limiters = {
        "chat": RateLimiter(settings.rate_limit_per_minute_chat, 60),
        "run": RateLimiter(settings.rate_limit_per_minute_run, 60),
    }
    application.state.hint_policy = HintPolicy()

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
    application.state.rag_service = rag_service

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
