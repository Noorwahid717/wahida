"""Application settings module using pydantic-settings."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from .env file
env_file_path = Path("/home/noah/project/wahida/.env")
load_dotenv(env_file_path)


class Settings(BaseSettings):
    """Centralised configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Wahida API"
    backend_cors_origins: str = "http://localhost:3000"
    postgres_dsn: str | None = None
    redis_url: str | None = None
    judge0_url: str | None = None
    openai_api_key: str | None = None
    google_gemini_api_key: str | None = None
    posthog_api_key: str | None = None
    moderation_blocklist_path: str | None = None
    rate_limit_per_minute_chat: int = 20
    rate_limit_per_minute_run: int = 10
    supabase_url: str | None = None
    supabase_anon_key: str | None = None


@lru_cache()
def get_settings() -> Settings:
    """Return a cached settings instance."""

    return Settings()


settings = get_settings()

__all__ = ["Settings", "get_settings", "settings"]
