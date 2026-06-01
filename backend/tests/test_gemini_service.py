"""
TDD Tests: Gemini Service Analysis (extract_json & calculate_business_metrics)
Scenarios: GS-01 through GS-13
"""
import pytest
import json
from unittest.mock import patch, AsyncMock
from app.services.gemini_service_analysis import extract_json, calculate_business_metrics
from app.schemas.schemas import AreaDistribution


class TestExtractJson:
    """Unit tests for JSON extraction from Gemini responses"""

    def test_gs01_plain_json_string(self):
        """GS-01: Extract JSON dari plain JSON string"""
        result = extract_json('{"key": "val"}')
        assert result == {"key": "val"}

    def test_gs02_json_from_markdown_code_block(self):
        """GS-02: Extract JSON dari markdown code block"""
        text = '```json\n{"a": 1}\n```'
        result = extract_json(text)
        assert result == {"a": 1}

    def test_gs03_json_from_mixed_text(self):
        """GS-03: Extract JSON dari teks campuran"""
        text = 'Here is the result: {"x": 10} and some more text'
        result = extract_json(text)
        assert result == {"x": 10}

    def test_gs04_no_json_raises_error(self):
        """GS-04: Extract JSON dari string tanpa JSON → ValueError"""
        with pytest.raises(ValueError, match="No JSON found"):
            extract_json("no json here at all")

    def test_gs05_invalid_json_raises_error(self):
        """GS-05: Extract JSON invalid → error"""
        with pytest.raises((ValueError, json.JSONDecodeError)):
            extract_json('{"broken": ')

    def test_gs02b_nested_json(self):
        """GS-02b: Extract nested JSON correctly"""
        text = '```json\n{"outer": {"inner": 42}}\n```'
        result = extract_json(text)
        assert result == {"outer": {"inner": 42}}


class TestCalculateBusinessMetrics:
    """Unit tests for business metrics calculation"""

    @pytest.fixture
    def base_area_distribution(self):
        return AreaDistribution(
            residential=60,
            road=20,
            openSpace=20,
            estimated_population_density=5000,
            competitor_density_estimate="medium",
            reasoning="Test reasoning with valid data"
        )

    @pytest.fixture
    def base_business_params(self):
        return {
            "operatingHours": 12,
            "buildingWidth": 5,
            "productPrice": 20000
        }

    @pytest.fixture
    def base_metadata(self):
        return {
            "center": {"lat": -6.2, "lng": 106.81},
            "zoom": 17,
            "width": 800,
            "height": 600,
            "scale": 0.5
        }

    @pytest.mark.asyncio
    @patch("app.services.gemini_service_analysis.apply_weather_to_apt")
    async def test_gs06_valid_metrics_calculation(self, mock_weather, base_area_distribution, base_business_params, base_metadata):
        """GS-06: Business metrics — revenue calculation valid"""
        mock_weather.return_value = (50000, "clear")  # Mocked APT after weather

        result = await calculate_business_metrics(
            base_area_distribution, base_business_params, base_metadata
        )

        assert "monthlyRevenue" in result
        assert "yearlyRevenue" in result
        assert "dailyRevenue" in result
        assert "locationScore" in result
        assert "riskScore" in result
        assert "confidenceLevel" in result
        assert "tppd" in result
        assert "areaData" in result

    @pytest.mark.asyncio
    @patch("app.services.gemini_service_analysis.apply_weather_to_apt")
    async def test_gs07_low_buyers_score_penalty(self, mock_weather, base_business_params, base_metadata):
        """GS-07: Business metrics — low buyers → score penalty (× 0.85)"""
        # Use very low density to force low buyer count
        low_density_area = AreaDistribution(
            residential=5,
            road=5,
            openSpace=90,
            estimated_population_density=100,
            competitor_density_estimate="low",
            reasoning="Low density test"
        )
        mock_weather.return_value = (10, "clear")  # Very low APT

        result = await calculate_business_metrics(
            low_density_area, base_business_params, base_metadata
        )

        # When buyers < 20, the raw_score is multiplied by 0.85
        # We verify that locationScore is valid (between 1.0 and 9.5)
        assert 1.0 <= result["locationScore"] <= 9.5

    @pytest.mark.asyncio
    @patch("app.services.gemini_service_analysis.apply_weather_to_apt")
    async def test_gs08_competitor_low_factor(self, mock_weather, base_business_params, base_metadata):
        """GS-08: Business metrics — competitor 'low' → factor 1.0"""
        area = AreaDistribution(
            residential=60, road=20, openSpace=20,
            estimated_population_density=5000,
            competitor_density_estimate="low",
            reasoning="Test"
        )
        mock_weather.return_value = (50000, "clear")

        result = await calculate_business_metrics(area, base_business_params, base_metadata)
        # Low competition should yield a higher score than high competition
        score_low = result["locationScore"]

        area_high = AreaDistribution(
            residential=60, road=20, openSpace=20,
            estimated_population_density=5000,
            competitor_density_estimate="high",
            reasoning="Test"
        )
        result_high = await calculate_business_metrics(area_high, base_business_params, base_metadata)
        score_high = result_high["locationScore"]

        assert score_low >= score_high

    @pytest.mark.asyncio
    @patch("app.services.gemini_service_analysis.apply_weather_to_apt")
    async def test_gs09_competitor_high_factor(self, mock_weather, base_business_params, base_metadata):
        """GS-09: Business metrics — competitor 'high' → factor 0.3"""
        area = AreaDistribution(
            residential=60, road=20, openSpace=20,
            estimated_population_density=5000,
            competitor_density_estimate="high",
            reasoning="Test"
        )
        mock_weather.return_value = (50000, "clear")

        result = await calculate_business_metrics(area, base_business_params, base_metadata)
        # High competition: competitor_factor = 0.3
        # Should still produce a valid score
        assert 1.0 <= result["locationScore"] <= 9.5

    @pytest.mark.asyncio
    @patch("app.services.gemini_service_analysis.apply_weather_to_apt")
    async def test_gs10_confidence_high(self, mock_weather, base_business_params, base_metadata):
        """GS-10: Business metrics — confidence 'High' when density > 100 and road > 0"""
        area = AreaDistribution(
            residential=60, road=20, openSpace=20,
            estimated_population_density=5000,  # > 100
            competitor_density_estimate="medium",
            reasoning="Valid reasoning from Gemini AI analysis"  # No fallback keyword
        )
        mock_weather.return_value = (50000, "clear")

        result = await calculate_business_metrics(area, base_business_params, base_metadata)
        assert result["confidenceLevel"] == "High"

    @pytest.mark.asyncio
    @patch("app.services.gemini_service_analysis.apply_weather_to_apt")
    async def test_gs11_confidence_low_on_fallback(self, mock_weather, base_business_params, base_metadata):
        """GS-11: Business metrics — confidence 'Low' when reasoning contains 'Fallback'"""
        area = AreaDistribution(
            residential=60, road=20, openSpace=20,
            estimated_population_density=5000,
            competitor_density_estimate="medium",
            reasoning="Fallback: AI Analysis Failed - some error"
        )
        mock_weather.return_value = (50000, "clear")

        result = await calculate_business_metrics(area, base_business_params, base_metadata)
        assert result["confidenceLevel"] == "Low"

    @pytest.mark.asyncio
    @patch("app.services.gemini_service_analysis.apply_weather_to_apt")
    async def test_gs12_score_capped_at_9_5(self, mock_weather, base_business_params, base_metadata):
        """GS-12: Business metrics — score capped at 9.5 (extreme revenue)"""
        area = AreaDistribution(
            residential=99, road=1, openSpace=0,
            estimated_population_density=50000,  # Extremely high
            competitor_density_estimate="low",
            reasoning="Valid reasoning"
        )
        mock_weather.return_value = (99999999, "clear")  # Extremely high APT

        result = await calculate_business_metrics(area, base_business_params, base_metadata)
        assert result["locationScore"] <= 9.5

    @pytest.mark.asyncio
    @patch("app.services.gemini_service_analysis.apply_weather_to_apt")
    async def test_gs13_score_minimum_1_0(self, mock_weather, base_business_params, base_metadata):
        """GS-13: Business metrics — score minimum 1.0 (extremely low scenario)"""
        area = AreaDistribution(
            residential=1, road=1, openSpace=98,
            estimated_population_density=1,  # Extremely low
            competitor_density_estimate="high",
            reasoning="Fallback: test"
        )
        mock_weather.return_value = (1, "storm")  # Minimal APT

        result = await calculate_business_metrics(area, base_business_params, base_metadata)
        assert result["locationScore"] >= 1.0
