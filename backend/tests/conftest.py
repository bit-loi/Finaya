"""
Shared test fixtures and configuration for Finaya backend tests
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from app.api.v1.auth import get_current_user, get_current_user_optional
from app.schemas.schemas import User


# ─── Mock User Fixtures ───────────────────────────────────────

def _create_test_user():
    """Create a test user for dependency override"""
    return User(
        id="test_user_123",
        email="test@finaya.local",
        full_name="Tester Finaya",
        is_active=True,
        created_at="2024-01-01T00:00:00Z"
    )

def override_get_current_user():
    return _create_test_user()

def override_get_current_user_optional():
    return _create_test_user()


# ─── App Dependency Overrides ─────────────────────────────────

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_current_user_optional] = override_get_current_user_optional


# ─── Fixtures ─────────────────────────────────────────────────

@pytest.fixture
def client():
    """TestClient with lifespan events triggered"""
    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_user():
    """Returns a test User schema object"""
    return _create_test_user()

@pytest.fixture
def sample_business_params():
    """Sample business parameters for testing"""
    return {
        "operatingHours": 12,
        "buildingWidth": 5,
        "productPrice": 20000
    }

@pytest.fixture
def sample_screenshot_metadata():
    """Sample screenshot metadata for testing"""
    return {
        "center": {"lat": -6.2, "lng": 106.81},
        "zoom": 17,
        "width": 800,
        "height": 600,
        "scale": 0.5
    }
