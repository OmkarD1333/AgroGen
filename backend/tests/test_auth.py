import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.database import Base
from app.dependencies.db import get_db
from app.main import app
from app.database.models import User
from app.core.config import settings

# In-memory SQLite database for test isolation
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(bind=test_engine)

    def tearDown(self):
        Base.metadata.drop_all(bind=test_engine)

    def test_root_health_check(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "online")
        self.assertIn("auth_endpoints", data)

    def test_google_url_unconfigured(self):
        old_id = settings.google_client_id
        try:
            settings.google_client_id = "your_google_client_id.apps.googleusercontent.com"
            response = client.get("/api/v1/auth/google/url")
            self.assertEqual(response.status_code, 400)
            self.assertIn("Google OAuth is not configured", response.json()["detail"])
        finally:
            settings.google_client_id = old_id

    def test_google_url_configured(self):
        old_id = settings.google_client_id
        old_uri = settings.google_redirect_uri
        try:
            settings.google_client_id = "real-client-id-123.apps.googleusercontent.com"
            settings.google_redirect_uri = "http://localhost:8000/api/v1/auth/google/callback"
            response = client.get("/api/v1/auth/google/url?state=test_state_123")
            self.assertEqual(response.status_code, 200)
            url = response.json()["url"]
            self.assertIn("accounts.google.com", url)
            self.assertIn("real-client-id-123.apps.googleusercontent.com", url)
            self.assertIn("test_state_123", url)
        finally:
            settings.google_client_id = old_id
            settings.google_redirect_uri = old_uri

    def test_google_login_redirect(self):
        old_id = settings.google_client_id
        old_uri = settings.google_redirect_uri
        try:
            settings.google_client_id = "real-client-id-123.apps.googleusercontent.com"
            settings.google_redirect_uri = "http://localhost:8000/api/v1/auth/google/callback"
            response = client.get("/api/v1/auth/google/login?state=csrf_123", follow_redirects=False)
            self.assertEqual(response.status_code, 307)
            self.assertIn("accounts.google.com", response.headers["location"])
        finally:
            settings.google_client_id = old_id
            settings.google_redirect_uri = old_uri

    def test_google_verify_missing_token(self):
        response = client.post("/api/v1/auth/google/verify", json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing Google credential", response.json()["detail"])

    def test_google_verify_success(self):
        mock_payload = {
            "google_id": "google_sub_98765",
            "email": "farmer_ramesh@example.com",
            "full_name": "Ramesh Patil",
            "avatar_url": "https://lh3.googleusercontent.com/a/test-avatar",
            "email_verified": True,
        }

        with patch("app.routes.auth.verify_google_credential", return_value=mock_payload):
            response = client.post(
                "/api/v1/auth/google/verify",
                json={"credential": "mock_google_id_token"},
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("access_token", data)
            self.assertEqual(data["token_type"], "bearer")
            self.assertEqual(data["user"]["email"], "farmer_ramesh@example.com")
            self.assertEqual(data["user"]["full_name"], "Ramesh Patil")
            self.assertEqual(data["user"]["role"], "farmer")
            self.assertEqual(data["user"]["avatar_url"], "https://lh3.googleusercontent.com/a/test-avatar")
            self.assertEqual(data["user"]["auth_provider"], "google")

            # Verify in DB
            db = TestingSessionLocal()
            user = db.query(User).filter(User.email == "farmer_ramesh@example.com").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.google_id, "google_sub_98765")
            db.close()

    def test_google_callback_flow(self):
        mock_tokens = {"access_token": "mock_google_access_token"}
        mock_profile = {
            "sub": "google_sub_112233",
            "email": "farmer_suresh@example.com",
            "name": "Suresh Deshmukh",
            "picture": "https://lh3.googleusercontent.com/a/suresh.jpg",
        }

        with patch("app.routes.auth.exchange_code_for_tokens", return_value=mock_tokens), \
             patch("app.routes.auth.get_google_user_info_via_token", return_value=mock_profile):

            response = client.get(
                "/api/v1/auth/google/callback?code=mock_code_abc",
                follow_redirects=False,
            )

            self.assertEqual(response.status_code, 307)
            redirect_url = response.headers["location"]
            self.assertIn("/auth/callback?", redirect_url)
            self.assertIn("token=", redirect_url)
            self.assertTrue("farmer_suresh%40example.com" in redirect_url or "farmer_suresh@example.com" in redirect_url)

    def test_get_current_user_profile(self):
        # 1. Register a user
        reg_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "anita@example.com",
                "full_name": "Anita Shinde",
                "password": "Password123!",
                "role": "farmer",
            },
        )
        self.assertEqual(reg_response.status_code, 201)
        token = reg_response.json()["access_token"]

        # 2. Access /me with token
        headers = {"Authorization": f"Bearer {token}"}
        me_response = client.get("/api/v1/auth/me", headers=headers)
        self.assertEqual(me_response.status_code, 200)
        data = me_response.json()
        self.assertEqual(data["email"], "anita@example.com")
        self.assertEqual(data["full_name"], "Anita Shinde")
        self.assertEqual(data["role"], "farmer")

        # 3. Access /me without token fails with 401
        unauth_response = client.get("/api/v1/auth/me")
        self.assertEqual(unauth_response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
