from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Wahida API"
    openai_api_key: str | None = None
    postgres_dsn: str | None = None
    redis_url: str | None = None
    judge0_url: str | None = None
    posthog_api_key: str | None = None


settings = Settings()
