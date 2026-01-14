"""Configuration settings for TerryAnn Core."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # App settings
    app_name: str = "TerryAnn Core"
    debug: bool = False
    api_version: str = "v1"

    # Auth settings
    jwt_secret: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60

    # SynthWell backend (intelligence layer)
    synthwell_api_url: str = "https://synthwell-prototype-production.up.railway.app"
    synthwell_api_key: str = ""

    # Supabase (for session storage)
    supabase_url: str = ""
    supabase_service_key: str = ""  # Service key for server-side operations

    # Claude API (for conversation)
    anthropic_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
