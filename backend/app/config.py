import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- Supabase ---
    database_url: str = os.environ.get("DATABASE_URL", "")

    # --- Code Execution (Judge0 via RapidAPI) ---
    rapidapi_key: str = os.environ.get("RAPIDAPI_KEY", "")

    # --- Server ---
    host: str = "0.0.0.0"
    port: int = 3000
    reload: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()