from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from app.routes.auth import user_router  

app = FastAPI()
# app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

app.include_router(user_router, prefix="/api")