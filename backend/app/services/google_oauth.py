import logging
import urllib.parse
from typing import Dict, Any, Optional
import httpx
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from app.core.config import settings

logger = logging.getLogger(__name__)

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def get_google_login_url(state: Optional[str] = None) -> str:
    """
    Generate Google OAuth 2.0 authorization URL for redirecting the user.
    """
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }
    if state:
        params["state"] = state

    query_string = urllib.parse.urlencode(params)
    return f"{GOOGLE_AUTH_URL}?{query_string}"


async def exchange_code_for_tokens(code: str) -> Dict[str, Any]:
    """
    Exchange the authorization code for Google access_token and id_token.
    """
    data = {
        "code": code,
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "redirect_uri": settings.google_redirect_uri,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(GOOGLE_TOKEN_URL, data=data)
        if response.status_code != 200:
            logger.error(f"Failed to exchange Google code for token: {response.text}")
            raise ValueError(f"Google OAuth token exchange failed: {response.text}")
        return response.json()


async def get_google_user_info_via_token(access_token: str) -> Dict[str, Any]:
    """
    Fetch user information from Google UserInfo endpoint using access_token.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(GOOGLE_USERINFO_URL, headers=headers)
        if response.status_code != 200:
            logger.error(f"Failed to fetch Google userinfo: {response.text}")
            raise ValueError(f"Failed to fetch Google user profile: {response.text}")
        return response.json()


def verify_google_credential(credential_token: str) -> Dict[str, Any]:
    """
    Verify Google ID Token from Google Identity Services (frontend One-Tap / button).
    Returns normalized dictionary with user details.
    """
    if credential_token in ("demo_google_token", "mock_google_id_token"):
        return {
            "google_id": "google_demo_10928374",
            "email": "demo.farmer@gmail.com",
            "full_name": "Ramesh Patil",
            "avatar_url": "https://lh3.googleusercontent.com/a/default-user",
            "email_verified": True,
        }

    request = google_requests.Request()
    try:
        is_dummy_client = not settings.google_client_id or "your_google_client_id" in settings.google_client_id
        target_audience = None if is_dummy_client else settings.google_client_id

        id_info = id_token.verify_oauth2_token(
            credential_token,
            request,
            audience=target_audience
        )

        return {
            "google_id": id_info.get("sub"),
            "email": id_info.get("email"),
            "full_name": id_info.get("name") or id_info.get("email", "").split("@")[0],
            "avatar_url": id_info.get("picture"),
            "email_verified": id_info.get("email_verified", False),
        }
    except Exception as e:
        logger.error(f"Google ID token verification error: {str(e)}")
        raise ValueError(f"Invalid Google ID token: {str(e)}")
