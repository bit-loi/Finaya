"""
TDD Tests: User Service
Scenarios: US-01 through US-07
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime
from app.services.user_service import UserService
from app.schemas.schemas import UserCreate
from app.core.exceptions import ValidationError, DatabaseError, AuthenticationError


@pytest.fixture
def user_service():
    return UserService()


@pytest.fixture
def valid_user_data():
    return UserCreate(email="new@test.com", full_name="New User", password="pass123")


@pytest.fixture
def mock_db_user():
    return {
        "id": "user_001",
        "email": "test@test.com",
        "full_name": "Test User",
        "password_hash": "firebase_managed_account",
        "is_active": True,
        "created_at": datetime(2024, 1, 1),
    }


class TestCreateUser:
    @pytest.mark.asyncio
    async def test_us01_create_user_success(self, user_service, valid_user_data):
        """US-01: Create user sukses"""
        with patch.object(user_service.user_repo, 'check_email_exists', new_callable=AsyncMock) as mock_check, \
             patch.object(user_service.user_repo, 'create_user', new_callable=AsyncMock) as mock_create:
            mock_check.return_value = False
            mock_create.return_value = {
                "id": "new_user_001", "email": "new@test.com",
                "full_name": "New User", "is_active": True,
                "created_at": datetime(2024, 1, 1)
            }
            result = await user_service.create_user(valid_user_data)
            assert result.id == "new_user_001"
            assert result.email == "new@test.com"

    @pytest.mark.asyncio
    async def test_us02_create_user_email_exists(self, user_service, valid_user_data):
        """US-02: Create user email sudah ada → ValidationError"""
        with patch.object(user_service.user_repo, 'check_email_exists', new_callable=AsyncMock) as mock_check:
            mock_check.return_value = True
            with pytest.raises(ValidationError):
                await user_service.create_user(valid_user_data)

    @pytest.mark.asyncio
    async def test_us03_create_user_db_fails(self, user_service, valid_user_data):
        """US-03: Create user DB gagal → DatabaseError"""
        with patch.object(user_service.user_repo, 'check_email_exists', new_callable=AsyncMock) as mock_check, \
             patch.object(user_service.user_repo, 'create_user', new_callable=AsyncMock) as mock_create:
            mock_check.return_value = False
            mock_create.return_value = None
            with pytest.raises(DatabaseError):
                await user_service.create_user(valid_user_data)


class TestAuthenticateUser:
    @pytest.mark.asyncio
    async def test_us04_firebase_account_rejects_password(self, user_service, mock_db_user):
        """US-04: Authenticate with firebase-managed account → AuthenticationError"""
        with patch.object(user_service.user_repo, 'get_by_email', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_db_user
            with pytest.raises(AuthenticationError):
                await user_service.authenticate_user("test@test.com", "password")

    @pytest.mark.asyncio
    async def test_us05_authenticate_user_not_found(self, user_service):
        """US-05: Authenticate user not found → None"""
        with patch.object(user_service.user_repo, 'get_by_email', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = None
            result = await user_service.authenticate_user("unknown@test.com", "pass")
            assert result is None


class TestGetUserByEmail:
    @pytest.mark.asyncio
    async def test_us06_get_user_found(self, user_service, mock_db_user):
        """US-06: Get user by email found"""
        with patch.object(user_service.user_repo, 'get_by_email', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_db_user
            result = await user_service.get_user_by_email("test@test.com")
            assert result is not None
            assert result.email == "test@test.com"

    @pytest.mark.asyncio
    async def test_us07_get_user_not_found(self, user_service):
        """US-07: Get user by email not found"""
        with patch.object(user_service.user_repo, 'get_by_email', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = None
            result = await user_service.get_user_by_email("unknown@test.com")
            assert result is None
