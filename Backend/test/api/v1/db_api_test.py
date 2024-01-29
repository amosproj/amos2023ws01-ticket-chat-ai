import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
from app.main import app

from app.dependency.repository import get_service_repository, get_category_repository


# Mock dependencies
@pytest.fixture
def mock_service_repository():
    service_repo = Mock()
    service_repo.read_services.return_value = [
        {'service_name': 'Service1'},
        {'service_name': 'Service2'}
    ]
    return service_repo


@pytest.fixture
def mock_category_repository():
    category_repo = Mock()
    category_repo.read_categories.return_value = [
        {'name': 'Category1'},
        {'name': 'Category2'}
    ]
    return category_repo


@pytest.fixture
def client(mock_service_repository, mock_category_repository):
    app.dependency_overrides[get_service_repository] = lambda: mock_service_repository
    app.dependency_overrides[get_category_repository] = lambda: mock_category_repository
    return TestClient(app)


# Tests
class TestAPI:
    def test_get_services(self, client):
        response = client.get("/api/v1/services")
        assert response.status_code == 200
        assert response.json() == ["Service1", "Service2"]

    def test_get_categories(self, client):
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        assert response.json() == ["Category1", "Category2"]
