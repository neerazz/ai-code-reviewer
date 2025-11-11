"""
Tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "AI Code Reviewer"
    assert "version" in data


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_analyze_code(client):
    """Test code analysis endpoint"""
    payload = {
        "code": "def hello():\n    print('Hello World')",
        "file_path": "test.py",
        "language": "python",
    }

    response = client.post("/api/v1/reviews/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data


def test_migration_templates(client):
    """Test migration templates endpoint"""
    response = client.get("/api/v1/migrations/templates")
    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert len(data["templates"]) > 0
