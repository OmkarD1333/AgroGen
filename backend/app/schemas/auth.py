from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=150)
    password: str = Field(..., min_length=6)
    phone: Optional[str] = None
    role: Optional[str] = Field(default="farmer", pattern="^(farmer|admin)$")
    preferred_lang: Optional[str] = "en"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class GoogleTokenRequest(BaseModel):
    """Payload sent by frontend when using Google Identity Services (GIS) / One-Tap."""
    credential: Optional[str] = Field(None, description="Google JWT ID token from Google One Tap / Button")
    id_token: Optional[str] = Field(None, description="Alternative alias for Google ID token")
    email: Optional[str] = Field(None, description="Direct user-selected Google email in dev mode")
    full_name: Optional[str] = Field(None, description="Direct user-selected Google name in dev mode")
    avatar_url: Optional[str] = Field(None, description="Optional avatar URL")


class GoogleCodeExchangeRequest(BaseModel):
    """Payload sent by frontend to exchange Google authorization code for JWT."""
    code: str


class GoogleAuthUrlResponse(BaseModel):
    """URL to redirect the user to for Google OAuth2 consent screen."""
    url: str


class UserResponse(BaseModel):
    id: int
    email: Optional[str] = None
    full_name: str
    role: Optional[str] = "farmer"
    phone: Optional[str] = None
    preferred_language: Optional[str] = "en"
    avatar_url: Optional[str] = None
    auth_provider: Optional[str] = "local"
    is_active: bool = True
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: Optional[int] = None
    full_name: Optional[str] = None
    user: Optional[UserResponse] = None
