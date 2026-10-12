# `backend/app/core/config.py`
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # ---------------------------------------------------------
    # Application
    # ---------------------------------------------------------
    app_name: str = "AgroGen AI"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True

    # ---------------------------------------------------------
    # API
    # ---------------------------------------------------------
    api_v1_prefix: str = "/api/v1"

    # ---------------------------------------------------------
    # Database
    # ---------------------------------------------------------
    database_url: str = Field(..., alias="DATABASE_URL")

    # ---------------------------------------------------------
    # JWT Authentication
    # ---------------------------------------------------------
    secret_key: str = Field(..., alias="SECRET_KEY")
    jwt_algorithm: str = Field(
        default="HS256",
        alias="JWT_ALGORITHM",
    )
    access_token_expire_minutes: int = Field(
        default=30,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    refresh_token_expire_days: int = Field(
        default=7,
        alias="REFRESH_TOKEN_EXPIRE_DAYS",
    )

    # ---------------------------------------------------------
    # Google Gemini
    # ---------------------------------------------------------
    gemini_api_key: str = Field(..., alias="GEMINI_API_KEY")
    gemini_model: str = Field(
        default="gemini-2.5-flash",
        alias="GEMINI_MODEL",
    )
    gemini_embedding_model: str = Field(
        default="models/gemini-embedding-001",
        alias="GEMINI_EMBEDDING_MODEL",
    )

    # ---------------------------------------------------------
    # ChromaDB
    # ---------------------------------------------------------
    chroma_persist_directory: str = Field(
        default="../rag/vector_db/chroma",
        alias="CHROMA_PERSIST_DIRECTORY",
    )
    chroma_collection_name: str = Field(
        default="agrogen_knowledge",
        alias="CHROMA_COLLECTION_NAME",
    )

    # ---------------------------------------------------------
    # LangSmith
    # ---------------------------------------------------------
    langsmith_api_key: str | None = Field(
        default=None,
        alias="LANGSMITH_API_KEY",
    )
    langsmith_project: str = Field(
        default="agrogen-ai",
        alias="LANGSMITH_PROJECT",
    )
    langsmith_tracing: bool = Field(
        default=False,
        alias="LANGSMITH_TRACING",
    )

    # ---------------------------------------------------------
    # Weather API
    # ---------------------------------------------------------
    openweather_api_key: str | None = Field(
        default=None,
        alias="OPENWEATHER_API_KEY",
    )

    # ---------------------------------------------------------
    # Market APIs
    # ---------------------------------------------------------
    agmarknet_api_key: str | None = Field(
        default=None,
        alias="AGMARKNET_API_KEY",
    )
    enam_api_key: str | None = Field(
        default=None,
        alias="ENAM_API_KEY",
    )

    # ---------------------------------------------------------
    # YOLO
    # ---------------------------------------------------------
    yolo_model_path: str = Field(
        default="../ml/models/trained/best.pt",
        alias="YOLO_MODEL_PATH",
    )
    yolo_confidence_threshold: float = Field(
        default=0.50,
        alias="YOLO_CONFIDENCE_THRESHOLD",
    )

    # ---------------------------------------------------------
    # File Upload
    # ---------------------------------------------------------
    max_upload_size_mb: int = Field(
        default=10,
        alias="MAX_UPLOAD_SIZE_MB",
    )
    allowed_image_types: str = Field(
        default="image/jpeg,image/png,image/webp",
        alias="ALLOWED_IMAGE_TYPES",
    )

    # ---------------------------------------------------------
    # CORS
    # ---------------------------------------------------------
    frontend_url: str = Field(
        default="http://localhost:5173",
        alias="FRONTEND_URL",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    Using lru_cache prevents loading and parsing the .env
    file repeatedly during application execution.
    """
    return Settings()


settings = get_settings()
