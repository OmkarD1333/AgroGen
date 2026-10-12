from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.database.models import User
from app.schemas.auth import RegisterRequest, LoginRequest, Token, UserResponse
from app.auth.security import hash_password, verify_password, create_access_token

user_router = APIRouter(prefix="/auth", tags=["auth"])

@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=hash_password(user_data.password),
        role=user_data.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = create_access_token(data={"sub": str(new_user.id), "role": new_user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": new_user.id,
        "role": new_user.role
    }

@user_router.post("/login", response_model=Token)
async def login_user(user_data: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if not db_user or not verify_password(user_data.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    token = create_access_token(data={"sub": str(db_user.id), "role": db_user.role})
    return {
        "access_token": token,
        "token_type": "bearer"
    }