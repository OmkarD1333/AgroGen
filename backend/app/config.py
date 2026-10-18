# backend/app/config.py
import os
from functools import lru_cache
from typing import List, Union
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Application
    app_name: str = "AgroGen AI"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True

    # API
    api_v1_prefix: str = Field(
        default="/api/v1",
        alias="API_V1_PREFIX",
    )

    # Google OAuth 2.0
    google_client_id: str = Field(
        default="your_google_client_id.apps.googleusercontent.com",
        alias="GOOGLE_CLIENT_ID",
    )
    google_client_secret: str = Field(
        default="your_google_client_secret",
        alias="GOOGLE_CLIENT_SECRET",
    )
    google_redirect_uri: str = Field(
        default="http://localhost:8000/api/v1/auth/google/callback",
        alias="GOOGLE_REDIRECT_URI",
    )

    # Database
    database_url: str = Field(
        default="postgresql://postgres:omkar1333@localhost:5432/agrogen",
        alias="DATABASE_URL",
    )

    # JWT Authentication
    secret_key: str = Field(
        default="(b}aK=iVT(lL&<PFMAQBIWdrt99c36e[E_HtEWs8ew)",
        alias="SECRET_KEY",
    )
    jwt_algorithm: str = Field(
        default="HS256",
        alias="JWT_ALGORITHM",
    )
    access_token_expire_minutes: int = Field(
        default=1440,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    refresh_token_expire_days: int = Field(
        default=7,
        alias="REFRESH_TOKEN_EXPIRE_DAYS",
    )

    # Google Gemini
    gemini_api_key: str = Field(
        default="",
        alias="GEMINI_API_KEY",
    )
    gemini_model: str = Field(
        default="gemini-2.5-flash",
        alias="GEMINI_MODEL",
    )
    gemini_embedding_model: str = Field(
        default="models/gemini-embedding-001",
        alias="GEMINI_EMBEDDING_MODEL",
    )

    # ChromaDB / RAG
    chroma_persist_directory: str = Field(
        default="../rag/vector_db/chroma",
        alias="CHROMA_PERSIST_DIRECTORY",
    )
    chroma_collection_name: str = Field(
        default="agrogen_knowledge",
        alias="CHROMA_COLLECTION_NAME",
    )

    # Weather
    openweather_api_key: str = Field(
        default="",
        alias="OPENWEATHER_API_KEY",
    )

    # Mandi / Market APIs
    agmarknet_api_key: str = Field(
        default="",
        alias="AGMARKNET_API_KEY",
    )
    enam_api_key: str = Field(
        default="",
        alias="ENAM_API_KEY",
    )

    # YOLO Model
    yolo_model_path: str = Field(
        default="../ml/weights/best.pt",
        alias="YOLO_MODEL_PATH",
    )
    yolo_confidence_threshold: float = Field(
        default=0.40,
        alias="YOLO_CONFIDENCE_THRESHOLD",
    )

    # Uploads & Storage
    max_upload_size_mb: int = Field(
        default=10,
        alias="MAX_UPLOAD_SIZE_MB",
    )
    upload_dir: str = Field(
        default="uploads",
        alias="UPLOAD_DIR",
    )

    # CORS
    frontend_url: str = Field(
        default="http://localhost:5173",
        alias="FRONTEND_URL",
    )

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

    model_config = SettingsConfigDict(
        env_file=(".env", "app/.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


settings = get_settings()