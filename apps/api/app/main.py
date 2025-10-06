from fastapi import FastAPI

from .config import settings
from .routers import chat, quiz, runner, progress


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name)
    application.include_router(chat.router, prefix="/api")
    application.include_router(quiz.router, prefix="/api")
    application.include_router(runner.router, prefix="/api")
    application.include_router(progress.router, prefix="/api")
    return application


app = create_app()


def run() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


__all__ = ["app", "create_app", "run"]
