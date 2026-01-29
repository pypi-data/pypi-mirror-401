"""Tests for API endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "trace_id" in data


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_readiness_check():
    """Test readiness check endpoint."""
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_trace_id_header():
    """Test that trace ID is returned in response headers."""
    response = client.get("/")
    assert "X-Trace-ID" in response.headers
    assert len(response.headers["X-Trace-ID"]) > 0
