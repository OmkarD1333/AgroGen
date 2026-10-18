from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database.database import engine, Base
import app.database.models  # ensure models are registered with Base

# Import all routers from app.routes
from app.routes.auth import user_router
from app.routes.farmer import farmer_router
from app.routes.crops import crops_router
from app.routes.disease import disease_router
from app.routes.weather import weather_router
from app.routes.market import market_router
from app.routes.schemes import schemes_router
from app.routes.chatbot import chatbot_router
from app.routes.yield_prediction import yield_router
from app.routes.voice import voice_router
from app.routes.notifications import notifications_router
from app.routes.recommendations import recommendations_router

# Automatically create database tables if they do not exist
try:
    Base.metadata.create_all(bind=engine)
    from sqlalchemy import text
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'farmer';"))
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;"))
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id VARCHAR(255) UNIQUE;"))
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(500);"))
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS auth_provider VARCHAR(50) DEFAULT 'local';"))
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();"))
        conn.execute(text("ALTER TABLE users ALTER COLUMN password_hash DROP NOT NULL;"))
except Exception as e:
    print(f"Note: Database table initialization skipped or deferred: {e}")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="High-Performance Asynchronous Agricultural Intelligence Engine for Smart Farming in Maharashtra.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]
if settings.frontend_url and settings.frontend_url not in allowed_origins:
    allowed_origins.append(settings.frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving for uploads (leaves, generated audio)
upload_dir = Path("uploads")
upload_dir.mkdir(parents=True, exist_ok=True)
(upload_dir / "audio").mkdir(parents=True, exist_ok=True)
(upload_dir / "disease").mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Health Check
@app.get("/", tags=["Health"])
async def root():
    """API health and root info."""
    api_prefix = getattr(settings, "api_v1_prefix", "/api/v1")
    return {
        "status": "online",
        "app": settings.app_name,
        "version": settings.app_version,
        "docs_url": "/docs",
        "auth_endpoints": {
            "google_login": f"{api_prefix}/auth/google/login",
            "google_url": f"{api_prefix}/auth/google/url",
            "google_verify": f"{api_prefix}/auth/google/verify",
            "me": f"{api_prefix}/auth/me",
        },
    }


@app.get("/health", tags=["system"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
    }


# Mount auth routes with /api/v1 prefix as well
api_v1 = getattr(settings, "api_v1_prefix", "/api/v1")
app.include_router(user_router, prefix=api_v1)

# Mount all routers under /api (matching both README and frontend)
for router in [
    user_router,
    farmer_router,
    crops_router,
    disease_router,
    weather_router,
    market_router,
    schemes_router,
    chatbot_router,
    yield_router,
    voice_router,
    notifications_router,
    recommendations_router,
]:
    app.include_router(router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)