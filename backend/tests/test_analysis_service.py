"""
TDD Tests: Analysis Service (CRUD with mocked repository)
Scenarios: AS-01 through AS-08
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime
from app.services.analysis_service import AnalysisService
from app.schemas.schemas import AnalysisCreate
from app.core.exceptions import ValidationError, DatabaseError


@pytest.fixture
def analysis_service():
    return AnalysisService()


@pytest.fixture
def valid_analysis_data():
    return AnalysisCreate(
        name="Test Analysis",
        location="-6.2,106.8",
        analysis_type="business",
        data={"locationScore": 8.5, "riskScore": 0.3, "monthlyRevenue": 50000000, "yearlyRevenue": 600000000}
    )


@pytest.fixture
def mock_db_analysis():
    return {
        "id": "analysis_001",
        "user_id": "user_001",
        "name": "Test Analysis",
        "location": "-6.2,106.8",
        "analysis_type": "business",
        "data": {"locationScore": 8.5},
        "gemini_analysis": {},
        "created_at": datetime(2024, 1, 1),
        "updated_at": datetime(2024, 1, 1),
    }


class TestCreateAnalysis:
    @pytest.mark.asyncio
    async def test_as01_create_success(self, analysis_service, valid_analysis_data, mock_db_analysis):
        """AS-01: Create analysis sukses"""
        with patch.object(analysis_service.analysis_repo, 'create_analysis', new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_db_analysis
            result = await analysis_service.create_analysis(valid_analysis_data, "user_001")
            assert result.id == "analysis_001"
            assert result.name == "Test Analysis"

    @pytest.mark.asyncio
    async def test_as02_create_without_name_raises_validation(self, analysis_service):
        """AS-02: Create analysis tanpa name → ValidationError"""
        invalid_data = AnalysisCreate(
            name="", location="-6.2,106.8",
            analysis_type="business", data={"key": "val"}
        )
        with pytest.raises(ValidationError):
            await analysis_service.create_analysis(invalid_data, "user_001")

    @pytest.mark.asyncio
    async def test_as03_create_repo_fails_raises_database_error(self, analysis_service, valid_analysis_data):
        """AS-03: Create analysis repo gagal → DatabaseError"""
        with patch.object(analysis_service.analysis_repo, 'create_analysis', new_callable=AsyncMock) as mock_create:
            mock_create.return_value = None
            with pytest.raises(DatabaseError):
                await analysis_service.create_analysis(valid_analysis_data, "user_001")


class TestGetAnalysis:
    @pytest.mark.asyncio
    async def test_as04_get_analysis_success(self, analysis_service, mock_db_analysis):
        """AS-04: Get analysis sukses"""
        with patch.object(analysis_service.analysis_repo, 'get_analysis_by_id_and_user', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_db_analysis
            result = await analysis_service.get_analysis("analysis_001", "user_001")
            assert result is not None
            assert result.id == "analysis_001"

    @pytest.mark.asyncio
    async def test_as05_get_analysis_not_found(self, analysis_service):
        """AS-05: Get analysis not found → None"""
        with patch.object(analysis_service.analysis_repo, 'get_analysis_by_id_and_user', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = None
            result = await analysis_service.get_analysis("unknown", "user_001")
            assert result is None


class TestGetUserAnalyses:
    @pytest.mark.asyncio
    async def test_as06_get_user_analyses_empty(self, analysis_service):
        """AS-06: Get user analyses empty list"""
        with patch.object(analysis_service.analysis_repo, 'get_by_user_id', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = []
            result = await analysis_service.get_user_analyses("user_001")
            assert result == []


class TestDeleteAnalysis:
    @pytest.mark.asyncio
    async def test_as07_delete_success(self, analysis_service):
        """AS-07: Delete analysis sukses"""
        with patch.object(analysis_service.analysis_repo, 'delete_analysis', new_callable=AsyncMock) as mock_del:
            mock_del.return_value = True
            result = await analysis_service.delete_analysis("analysis_001", "user_001")
            assert result is True

    @pytest.mark.asyncio
    async def test_as08_delete_fails_raises_database_error(self, analysis_service):
        """AS-08: Delete analysis gagal → DatabaseError"""
        with patch.object(analysis_service.analysis_repo, 'delete_analysis', new_callable=AsyncMock) as mock_del:
            mock_del.side_effect = Exception("DB connection lost")
            with pytest.raises(DatabaseError):
                await analysis_service.delete_analysis("analysis_001", "user_001")
