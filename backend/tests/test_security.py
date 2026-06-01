"""
TDD Tests: Security Manager
Scenarios: SC-01 through SC-11
"""
import pytest
from fastapi import HTTPException
from app.core.security import SecurityManager


class TestSanitizeInput:
    """Unit tests for input sanitization"""

    def test_sc01_removes_dangerous_characters(self):
        """SC-01: Sanitize input menghapus karakter <>{} $"""
        result = SecurityManager.sanitize_input("<script>alert(1)</script>")
        assert "<" not in result
        assert ">" not in result
        assert result == "scriptalert(1)/script"

    def test_sc02_normal_string_unchanged(self):
        """SC-02: Sanitize input string normal → tetap sama"""
        result = SecurityManager.sanitize_input("Hello World")
        assert result == "Hello World"

    def test_sc03_empty_string_returns_empty(self):
        """SC-03: Sanitize input string kosong → kosong"""
        result = SecurityManager.sanitize_input("")
        assert result == ""

    def test_sc01b_removes_dollar_and_braces(self):
        """SC-01b: Sanitize removes $ and {} characters"""
        result = SecurityManager.sanitize_input("${__import__('os')}")
        assert "$" not in result
        assert "{" not in result
        assert "}" not in result


class TestValidateApiKeyFormat:
    """Unit tests for API key format validation"""

    def test_sc04_valid_google_api_key(self):
        """SC-04: Validate Google API key format valid"""
        # Valid format: AIza + 35 alphanumeric characters
        valid_key = "AIza" + "X" * 35
        assert SecurityManager.validate_api_key_format(valid_key) is True

    def test_sc05_invalid_google_api_key(self):
        """SC-05: Validate Google API key format invalid"""
        assert SecurityManager.validate_api_key_format("invalid_key") is False
        assert SecurityManager.validate_api_key_format("") is False
        assert SecurityManager.validate_api_key_format("AIza_too_short") is False

    def test_sc06_non_google_provider_always_true(self):
        """SC-06: Validate API key non-google → always true"""
        assert SecurityManager.validate_api_key_format("any_key", "other") is True
        assert SecurityManager.validate_api_key_format("", "openai") is True


class TestCheckSafeCoordinates:
    """Unit tests for coordinate validation"""

    def test_sc07_valid_coordinates(self):
        """SC-07: Koordinat valid → True"""
        assert SecurityManager.check_safe_coordinates(-6.2, 106.8) is True
        assert SecurityManager.check_safe_coordinates(0, 0) is True
        assert SecurityManager.check_safe_coordinates(-90, -180) is True
        assert SecurityManager.check_safe_coordinates(90, 180) is True

    def test_sc08_latitude_out_of_range(self):
        """SC-08: Latitude out of range → HTTPException 400"""
        with pytest.raises(HTTPException) as exc_info:
            SecurityManager.check_safe_coordinates(91, 0)
        assert exc_info.value.status_code == 400

        with pytest.raises(HTTPException) as exc_info:
            SecurityManager.check_safe_coordinates(-91, 0)
        assert exc_info.value.status_code == 400

    def test_sc09_longitude_out_of_range(self):
        """SC-09: Longitude out of range → HTTPException 400"""
        with pytest.raises(HTTPException) as exc_info:
            SecurityManager.check_safe_coordinates(0, 181)
        assert exc_info.value.status_code == 400

        with pytest.raises(HTTPException) as exc_info:
            SecurityManager.check_safe_coordinates(0, -181)
        assert exc_info.value.status_code == 400


class TestMaskingEmail:
    """Unit tests for email masking"""

    def test_sc10_normal_email_masking(self):
        """SC-10: Email masking normal"""
        assert SecurityManager.masking_email("john@gmail.com") == "j***@gmail.com"
        assert SecurityManager.masking_email("alice@company.co.id") == "a***@company.co.id"

    def test_sc11_invalid_email_format(self):
        """SC-11: Email masking invalid format"""
        assert SecurityManager.masking_email("invalid") == "invalid_email"
        assert SecurityManager.masking_email("") == "invalid_email"
