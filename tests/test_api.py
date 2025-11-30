"""
Smoke tests for the FastAPI application.
Ensures health endpoints respond successfully without needing external services.
"""
from pathlib import Path
import sys

from fastapi.testclient import TestClient

# Make backend package importable when running tests from repo root
BACKEND_PATH = Path(__file__).resolve().parents[1] / "src" / "backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.append(str(BACKEND_PATH))

from api.main import app  # noqa: E402


client = TestClient(app)


def test_root_endpoint_returns_status():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "running"
    assert body.get("docs") == "/docs"


def test_health_endpoint_reports_healthy():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "healthy"
    assert body.get("service") == "ai-code-reviewer"
