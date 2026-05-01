import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.ratelimiter import rate_limiter

client = TestClient(app)

# Explicitly test endpoints

def test_health_check():
    """System test: Health endpoint should be accessible"""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

def test_root_endpoint():
    """System test: Root endpoint should be valid"""
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "version" in response.json()
        assert response.json()["message"] == "Welcome to Finaya API"

# Wait, rate limiter is initialized asynchronously in lifespan which TestClient supports in newer FastAPI versions > 0.100.0 if using `with TestClient(app) as client:`
def test_full_lifespan():
    """Test full app behavior wrapped in Context Manager to trigger Lifespan event"""
    with TestClient(app) as live_client:
        response = live_client.get("/health")
        assert response.status_code == 200
