"""
TDD Tests: Weather Probability Service
Scenarios: WP-01 through WP-14
"""
import pytest
from unittest.mock import patch
from app.services.weather_probability import (
    get_wmo_weather_state,
    apply_weather_to_apt,
    WEATHER_VIC,
)


class TestGetWmoWeatherState:
    """Unit tests for WMO weather code mapping"""

    def test_wp01_code_0_is_clear(self):
        """WP-01: WMO code 0 → clear"""
        assert get_wmo_weather_state(0) == "clear"

    def test_wp02_code_1_is_clear(self):
        """WP-02: WMO code 1 → clear"""
        assert get_wmo_weather_state(1) == "clear"

    def test_wp03_code_2_is_cloudy(self):
        """WP-03: WMO code 2 → cloudy"""
        assert get_wmo_weather_state(2) == "cloudy"

    def test_wp04_code_3_is_cloudy(self):
        """WP-04: WMO code 3 → cloudy"""
        assert get_wmo_weather_state(3) == "cloudy"

    def test_wp05_code_51_is_light_rain(self):
        """WP-05: WMO code 51 → light_rain"""
        assert get_wmo_weather_state(51) == "light_rain"

    def test_wp06_code_65_boundary_is_light_rain(self):
        """WP-06: WMO code 65 → light_rain (boundary)"""
        assert get_wmo_weather_state(65) == "light_rain"

    def test_wp07_code_80_is_heavy_rain(self):
        """WP-07: WMO code 80 → heavy_rain"""
        assert get_wmo_weather_state(80) == "heavy_rain"

    def test_wp08_code_82_is_heavy_rain(self):
        """WP-08: WMO code 82 → heavy_rain"""
        assert get_wmo_weather_state(82) == "heavy_rain"

    def test_wp09_code_95_is_storm(self):
        """WP-09: WMO code 95 → storm"""
        assert get_wmo_weather_state(95) == "storm"

    def test_wp10_code_99_is_storm(self):
        """WP-10: WMO code 99 → storm"""
        assert get_wmo_weather_state(99) == "storm"


class TestApplyWeatherToApt:
    """Unit tests for weather impact on APT"""

    @patch("app.services.weather_probability.get_real_weather", return_value="clear")
    def test_wp11_clear_weather_no_reduction(self, mock_weather):
        """WP-11: apply_weather clear → APT × 1.0"""
        result_apt, result_weather = apply_weather_to_apt(1000, lat=-6.2, lng=106.8)
        assert result_apt == 1000.0
        assert result_weather == "clear"

    @patch("app.services.weather_probability.get_real_weather", return_value="heavy_rain")
    def test_wp12_heavy_rain_reduces_to_60_percent(self, mock_weather):
        """WP-12: apply_weather heavy_rain → APT × 0.6"""
        result_apt, result_weather = apply_weather_to_apt(1000, lat=-6.2, lng=106.8)
        assert result_apt == 600.0
        assert result_weather == "heavy_rain"

    @patch("app.services.weather_probability.get_real_weather", return_value="storm")
    def test_wp13_storm_reduces_to_40_percent(self, mock_weather):
        """WP-13: apply_weather storm → APT × 0.4"""
        result_apt, result_weather = apply_weather_to_apt(1000, lat=-6.2, lng=106.8)
        assert result_apt == 400.0
        assert result_weather == "storm"

    def test_wp14_no_coordinates_uses_fallback(self):
        """WP-14: apply_weather tanpa koordinat → fallback random (returns valid tuple)"""
        result_apt, result_weather = apply_weather_to_apt(1000, None, None)

        # Should return a valid tuple
        assert isinstance(result_apt, float)
        assert isinstance(result_weather, str)
        assert result_weather in WEATHER_VIC
        # APT should be adjusted by the weather factor
        expected_apt = 1000 * WEATHER_VIC[result_weather]
        assert abs(result_apt - expected_apt) < 0.01
