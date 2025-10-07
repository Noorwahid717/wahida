from fastapi import FastAPI

from .config import settings
from .routers import chat, progress, quiz, runner
from .services.rag.container import get_pipeline
from .services.rag.pipeline import ingest_bulk
from .services.rag.sample_data import SAMPLE_MODULES


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name)
    application.include_router(chat.router, prefix="/api")
    application.include_router(quiz.router, prefix="/api")
    application.include_router(runner.router, prefix="/api")
    application.include_router(progress.router, prefix="/api")

    pipeline = get_pipeline()

    @application.on_event("startup")
    async def _bootstrap_rag() -> None:
        await ingest_bulk(pipeline, SAMPLE_MODULES)

    application.dependency_overrides[chat.get_rag_pipeline] = lambda: pipeline
    return application


app = create_app()


def run() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


__all__ = ["app", "create_app", "run"]
