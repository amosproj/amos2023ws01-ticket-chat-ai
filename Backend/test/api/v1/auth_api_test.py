import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import JWTError, jwt
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
from test.config.pytest import SKIP_TEST
from app.main import app
from app.dependency.repository import get_user_repository


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


# Mock dependencies
@pytest.fixture
def mock_user_repository():
    user_repo = Mock()
    user_repo.authenticate_user.return_value = True
    user_repo.read_users_by_email.return_value = [{"email_address": "test@example.com"}]
    return user_repo


@pytest.fixture
def client(mock_user_repository):
    app.dependency_overrides[get_user_repository] = lambda: mock_user_repository
    return TestClient(app)


def generate_valid_token():
    ALGORITHM = "HS256"
    data = {"sub": "test@example.com"}
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@pytest.mark.skipif(condition=SKIP_TEST, reason=".env on git")
class TestAPI:
    def test_login_for_access_token_success(self, client):
        response = client.post(
            "/api/v1/token",
            data={"username": "user@example.com", "password": "password"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_for_access_token_failure(self, client, mock_user_repository):
        # Configure the mock to return False for authentication
        mock_user_repository.authenticate_user.return_value = False
        response = client.post(
            "/api/v1/token",
            data={"username": "wrong@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 400

    def test_verify_token_success(self, client):
        valid_token = generate_valid_token()
        response = client.get(
            "/api/v1/verify-token", headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert response.status_code == 200

    def test_verify_token_failure(self, client):
        # Use an altered valid token for this test
        valid_token = generate_valid_token() + "invalid_part"
        response = client.get(
            "/api/v1/verify-token", headers={"Authorization": f"Bearer {valid_token}"}
        )
        assert response.status_code == 401
