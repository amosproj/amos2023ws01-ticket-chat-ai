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
        assert response.status_code == 402

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

    def test_signup_user_success(self, client, mock_user_repository):
        # Configure the mock with now existing user
        mock_user_repository.read_users_by_email.return_value = []
        response = client.post(
            "/api/v1/signup",
            json={
                "firstname": "Test",
                "lastname": "User",
                "email": "newuser@example.com",
                "password": "password",
                "officeLocation": "Berlin",
            },
        )
        assert response.status_code == 200

    def test_signup_user_email_exists(self, client, mock_user_repository):
        # Configure the mock to show that the email already exists
        mock_user_repository.read_users_by_email.return_value = [
            {"email_address": "existing@example.com"}
        ]
        response = client.post(
            "/api/v1/signup",
            json={
                "firstname": "Existing",
                "lastname": "User",
                "email": "existing@example.com",
                "password": "password",
                "officeLocation": "Berlin",
            },
        )
        assert response.status_code == 405

    def test_edit_user_success(self, client, mock_user_repository):
        # Configure the mock for successful authentication and non-existence of the new email
        mock_user_repository.authenticate_user.return_value = True
        mock_user_repository.read_users_by_email.side_effect = [[],[{"_id": "123", "email_address": "old@example.com"}]]
        response = client.post("/api/v1/edit", json={
            "old_password": "oldpassword",
            "old_email": "old@example.com",
            "first_name": "NewFirstName",
            "family_name": "NewLastName",
            "email": "new@example.com",
            "password": "newpassword",
            "location": "NewOffice"
        })
        assert response.status_code == 200

    def test_edit_user_failed_authentication(self, client, mock_user_repository):
        # Konfigurieren des Mocks für fehlgeschlagene Authentifizierung
        mock_user_repository.authenticate_user.return_value = False
        response = client.post("/api/v1/edit", json={
            "old_password": "oldpassword",
            "old_email": "old@example.com",
            "first_name": "NewFirstName",
            "family_name": "NewLastName",
            "email": "new@example.com",
            "password": "newpassword",
            "location": "NewOffice"
        })
        assert response.status_code == 402

    def test_edit_user_email_already_in_use(self, client, mock_user_repository):
        # Konfigurieren des Mocks für bestehende E-Mail
        mock_user_repository.authenticate_user.return_value = True
        mock_user_repository.read_users_by_email.return_value = [{"email_address": "new@example.com"}]
        response = client.post("/api/v1/edit", json={
            "old_password": "oldpassword",
            "old_email": "old@example.com",
            "first_name": "NewFirstName",
            "family_name": "NewLastName",
            "email": "new@example.com",
            "password": "newpassword",
            "location": "NewOffice"
        })
        assert response.status_code == 405

    def test_get_user_info_success(self, client, mock_user_repository):
        # Konfigurieren des Mocks für Benutzerabfrage
        mock_user_repository.read_users_by_email.return_value = [{"first_name": "Test", "family_name": "User", "location": "TestOffice"}]
        response = client.post("/api/v1/getuserinfo", json={"email": "test@example.com"})
        assert response.status_code == 200
        assert response.json() == {
            "first_name": "Test",
            "family_name": "User",
            "location": "TestOffice"
        }

