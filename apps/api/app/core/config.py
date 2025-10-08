"""Application settings module using pydantic-settings."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralised configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Wahida API"
    backend_cors_origins: list[str] = ["http://localhost:3000"]
    postgres_dsn: str | None = None
    redis_url: str | None = None
    judge0_url: str | None = None
    openai_api_key: str | None = None
    posthog_api_key: str | None = None
    moderation_blocklist_path: Path | None = None
    rate_limit_per_minute_chat: int = 20
    rate_limit_per_minute_run: int = 10


@lru_cache()
def get_settings() -> Settings:
    """Return a cached settings instance."""

    return Settings()


settings = get_settings()

__all__ = ["Settings", "get_settings", "settings"]
