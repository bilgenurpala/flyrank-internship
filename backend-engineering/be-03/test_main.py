from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from supabase import AuthApiError

from main import create_app


class FakeAuth:
    def __init__(self):
        self.user = SimpleNamespace(
            id="user-123",
            email="test@example.com",
            created_at="2026-07-28T12:00:00Z",
        )
        self.signed_out = False

    def sign_up(self, credentials):
        return SimpleNamespace(user=self.user)

    def sign_in_with_password(self, credentials):
        if credentials["password"] == "wrong-password":
            raise AuthApiError("Invalid login credentials", 400, None)
        session = SimpleNamespace(
            access_token="valid-access-token",
            refresh_token="valid-refresh-token",
        )
        return SimpleNamespace(session=session)

    def get_user(self, token):
        if token != "valid-access-token":
            raise AuthApiError("Invalid JWT", 401, None)
        return SimpleNamespace(user=self.user)

    def sign_out(self):
        self.signed_out = True


@pytest.fixture
def auth():
    return FakeAuth()


@pytest.fixture
def client(auth, monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "test-anon-key")
    application = create_app(SimpleNamespace(auth=auth))
    with TestClient(application) as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "connected to Supabase",
    }


def test_signup_and_login(client):
    credentials = {"email": "test@example.com", "password": "password123"}
    signup = client.post("/auth/signup", json=credentials)
    login = client.post("/auth/login", json=credentials)
    assert signup.status_code == 201
    assert signup.json()["user"]["id"] == "user-123"
    assert login.status_code == 200
    assert login.json() == {
        "access_token": "valid-access-token",
        "refresh_token": "valid-refresh-token",
    }


def test_auth_input_validation(client):
    signup = client.post("/auth/signup", json={"email": "test@example.com"})
    login = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "wrong-password"},
    )
    assert signup.status_code == 400
    assert signup.json() == {"error": "Email and password are required"}
    assert login.status_code == 401
    assert login.json() == {"error": "Invalid login credentials"}


def test_public_route_requires_no_token(client):
    response = client.get("/public/info")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome stranger! This info is public."
    }


@pytest.mark.parametrize(
    "headers, message",
    [
        ({}, "Access token required"),
        ({"Authorization": "Token invalid"}, "Access token required"),
        ({"Authorization": "Bearer invalid"}, "Invalid or expired token"),
    ],
)
def test_protected_route_rejects_invalid_auth(client, headers, message):
    response = client.get("/protected/profile", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"error": message}


def test_protected_routes_accept_valid_token(client):
    headers = {"Authorization": "Bearer valid-access-token"}
    profile = client.get("/protected/profile", headers=headers)
    dashboard = client.get("/protected/dashboard", headers=headers)
    assert profile.status_code == 200
    assert profile.json()["user"]["email"] == "test@example.com"
    assert dashboard.status_code == 200
    assert dashboard.json()["user_id"] == "user-123"


def test_logout_is_protected(client, auth):
    headers = {"Authorization": "Bearer valid-access-token"}
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 204
    assert response.content == b""
    assert auth.signed_out is True


def test_openapi_exposes_bearer_security(client):
    schema = client.get("/openapi.json").json()
    schemes = schema["components"]["securitySchemes"]
    assert schemes["HTTPBearer"] == {
        "type": "http",
        "description": "Supabase access token",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    protected_paths = (
        "/protected/profile",
        "/protected/dashboard",
        "/auth/logout",
    )
    for path in protected_paths:
        operation = next(iter(schema["paths"][path].values()))
        assert operation["security"] == [{"HTTPBearer": []}]
