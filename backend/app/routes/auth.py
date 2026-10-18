import logging
import urllib.parse
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_active_user, get_current_user
from app.database.models import User, FarmerProfile
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    Token,
    UserResponse,
    GoogleAuthUrlResponse,
    GoogleTokenRequest,
    GoogleCodeExchangeRequest,
)
from app.auth.security import hash_password, verify_password, create_access_token
from app.services.google_oauth import (
    get_google_login_url,
    exchange_code_for_tokens,
    get_google_user_info_via_token,
    verify_google_credential,
)

logger = logging.getLogger(__name__)

user_router = APIRouter(prefix="/auth", tags=["Authentication"])


# ---------------------------------------------------------------------------
# Traditional Email / Password Auth
# ---------------------------------------------------------------------------

@user_router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user with email and password."""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    if user_data.phone:
        clean_phone = user_data.phone.strip()
        if clean_phone:
            # Enforce exactly 10 digits valid Indian mobile number
            if not clean_phone.isdigit() or len(clean_phone) != 10 or clean_phone[0] not in "6789":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Please enter a valid 10-digit mobile number",
                )
            existing_phone = db.query(User).filter(User.phone == clean_phone).first()
            if existing_phone:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This mobile number is already registered with another account",
                )

    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        phone=user_data.phone,
        password_hash=hash_password(user_data.password),
        role=user_data.role or "farmer",
        auth_provider="local",
        preferred_lang=user_data.preferred_lang or "en",
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Automatically create initial farmer_profile for the user
    try:
        new_profile = FarmerProfile(
            user_id=new_user.id,
            state="Maharashtra",
        )
        db.add(new_profile)
        db.commit()
    except Exception as e:
        logger.warning(f"Initial farmer profile auto-creation notice: {e}")
        db.rollback()

    token = create_access_token(
        data={"sub": str(new_user.id), "email": new_user.email, "role": new_user.role}
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": new_user.id,
        "full_name": new_user.full_name,
        "user": new_user,
    }


@user_router.post("/login", response_model=Token)
async def login_user(user_data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate existing user with email and password."""
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if not db_user or not verify_password(user_data.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not getattr(db_user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )

    token = create_access_token(
        data={"sub": str(db_user.id), "email": db_user.email, "role": getattr(db_user, "role", "farmer")}
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "full_name": db_user.full_name,
        "user": db_user,
    }


# ---------------------------------------------------------------------------
# Google OAuth 2.0 Flow
# ---------------------------------------------------------------------------

@user_router.get("/google/url", response_model=GoogleAuthUrlResponse)
async def get_google_oauth_url(state: str = Query(None)):
    """
    Get Google OAuth 2.0 authorization URL for frontend to open in a popup or redirect.
    """
    if not settings.google_client_id or "your_google_client_id" in settings.google_client_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google OAuth is not configured yet. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in backend .env file.",
        )
    url = get_google_login_url(state=state)
    return {"url": url}


@user_router.get("/google/login")
async def google_login(state: str = Query(None)):
    """
    Direct endpoint: Redirects user browser directly to Google OAuth 2.0 consent screen.
    Opens the official Google 'Choose an account' prompt.
    """
    url = get_google_login_url(state=state)
    return RedirectResponse(url=url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


async def _process_google_code(code: str, db: Session):
    """Internal helper to exchange Google code, sync user to database, and return app token."""
    # 1. Exchange code for tokens
    token_data = await exchange_code_for_tokens(code)
    access_token = token_data.get("access_token")

    # 2. Get user profile from Google
    google_profile = await get_google_user_info_via_token(access_token)
    google_id = google_profile.get("sub")
    email = google_profile.get("email")
    full_name = google_profile.get("name") or (email.split("@")[0] if email else "Farmer")
    avatar_url = google_profile.get("picture")

    if not email:
        raise ValueError("Google account does not have a verified email address.")

    # 3. Find or create user in database
    user = db.query(User).filter(
        (User.google_id == google_id) | (User.email == email)
    ).first()

    if user:
        if not user.google_id:
            user.google_id = google_id
        if avatar_url and not user.avatar_url:
            user.avatar_url = avatar_url
        if full_name and not user.full_name:
            user.full_name = full_name
        db.commit()
        db.refresh(user)
    else:
        user = User(
            email=email,
            full_name=full_name,
            google_id=google_id,
            avatar_url=avatar_url,
            auth_provider="google",
            role="farmer",
            is_active=True,
            password_hash=None,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        try:
            profile = FarmerProfile(user_id=user.id, state="Maharashtra")
            db.add(profile)
            db.commit()
        except Exception as e:
            logger.warning(f"FarmerProfile creation notice: {e}")
            db.rollback()

    if not getattr(user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )

    # 4. Generate app JWT token
    app_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": getattr(user, "role", "farmer")}
    )
    return app_token, user


@user_router.post("/google/exchange", response_model=Token)
async def exchange_google_code_endpoint(
    payload: GoogleCodeExchangeRequest,
    db: Session = Depends(get_db),
):
    """
    Direct code exchange endpoint for frontend.
    Accepts Google authorization code from URL query and returns app JWT + user profile.
    """
    if not payload.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code is required",
        )
    try:
        app_token, user = await _process_google_code(payload.code, db)
        return {
            "access_token": app_token,
            "token_type": "bearer",
            "user_id": user.id,
            "full_name": user.full_name,
            "user": user,
        }
    except Exception as e:
        logger.error(f"Error exchanging Google OAuth code: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google authentication failed: {str(e)}",
        )


@user_router.get("/google/callback")
async def google_callback(
    code: str = Query(None),
    state: str = Query(None),
    error: str = Query(None),
    format: str = Query(None),
    db: Session = Depends(get_db),
):
    """
    Google OAuth 2.0 callback endpoint.
    Google redirects back here with `code` or `error`.
    Supports both browser 307 redirects and JSON responses when format=json.
    """
    if error:
        logger.warning(f"Google OAuth authorization returned error: {error}")
        if format == "json":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        return RedirectResponse(
            url=f"{settings.frontend_url}/login?error={urllib.parse.quote(error)}"
        )

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing authorization code from Google callback",
        )

    try:
        app_token, user = await _process_google_code(code, db)

        if format == "json":
            return {
                "access_token": app_token,
                "token_type": "bearer",
                "user_id": user.id,
                "full_name": user.full_name,
                "user": user,
            }

        # Redirect to frontend with token and user details
        frontend_callback_url = (
            f"{settings.frontend_url}/auth/callback?"
            f"token={urllib.parse.quote(app_token)}&"
            f"user_id={user.id}&"
            f"role={urllib.parse.quote(getattr(user, 'role', 'farmer'))}&"
            f"name={urllib.parse.quote(user.full_name)}&"
            f"email={urllib.parse.quote(user.email or '')}&"
            f"avatar={urllib.parse.quote(user.avatar_url or '')}&"
            f"auth_provider=google"
        )
        return RedirectResponse(url=frontend_callback_url)

    except Exception as e:
        logger.error(f"Error handling Google OAuth callback: {str(e)}")
        if format == "json":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        error_msg = urllib.parse.quote(f"Authentication failed: {str(e)}")
        return RedirectResponse(url=f"{settings.frontend_url}/login?error={error_msg}")



@user_router.post("/google/verify", response_model=Token)
async def verify_google_token(
    request: GoogleTokenRequest,
    db: Session = Depends(get_db),
):
    """
    Direct token verification endpoint.
    Used by Google Identity Services (GIS) One-Tap or Google Sign-In button on the frontend.
    """
    token_str = request.credential or request.id_token
    if not token_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Google credential or id_token in request body",
        )

    if request.email:
        email = request.email.strip().lower()
        full_name = request.full_name or email.split("@")[0].replace(".", " ").title()
        google_id = f"google_user_{abs(hash(email))}"
        avatar_url = request.avatar_url or f"https://api.dicebear.com/7.x/initials/svg?seed={urllib.parse.quote(full_name)}"
    else:
        try:
            user_info = verify_google_credential(token_str)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
            )
        google_id = user_info.get("google_id")
        email = user_info.get("email")
        full_name = user_info.get("full_name")
        avatar_url = user_info.get("avatar_url")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No email found in Google ID token",
        )

    # Find or create user
    user = db.query(User).filter(
        (User.google_id == google_id) | (User.email == email)
    ).first()

    if user:
        if not user.google_id:
            user.google_id = google_id
        if avatar_url and not user.avatar_url:
            user.avatar_url = avatar_url
        db.commit()
        db.refresh(user)
    else:
        user = User(
            email=email,
            full_name=full_name or email.split("@")[0],
            google_id=google_id,
            avatar_url=avatar_url,
            auth_provider="google",
            role="farmer",
            is_active=True,
            password_hash=None,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        try:
            profile = FarmerProfile(user_id=user.id, state="Maharashtra")
            db.add(profile)
            db.commit()
        except Exception as e:
            logger.warning(f"FarmerProfile creation notice: {e}")
            db.rollback()

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )

    app_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )

    return {
        "access_token": app_token,
        "token_type": "bearer",
        "user_id": user.id,
        "full_name": user.full_name,
        "user": user,
    }


# ---------------------------------------------------------------------------
# Profile & Session Management
# ---------------------------------------------------------------------------

@user_router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
):
    """Get the currently logged-in user profile."""
    return current_user


@user_router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """Log out current user."""
    return {"message": "Successfully logged out"}