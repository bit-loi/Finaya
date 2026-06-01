"""
TDD Tests: Pydantic Schemas
Scenarios: SM-01 through SM-07
"""
import pytest
from pydantic import ValidationError as PydanticValidationError
from app.schemas.schemas import (
    AreaDistribution, AnalysisCreate, UserCreate, FirebaseLogin, Token
)


class TestAreaDistribution:
    def test_sm01_valid_construction(self):
        area = AreaDistribution(
            residential=60, road=20, openSpace=20,
            estimated_population_density=5000,
            competitor_density_estimate="medium",
            reasoning="test"
        )
        assert area.residential == 60
        assert area.road == 20

    def test_sm02_missing_field_raises_error(self):
        with pytest.raises(PydanticValidationError):
            AreaDistribution(road=20, openSpace=20,
                estimated_population_density=5000,
                competitor_density_estimate="medium",
                reasoning="test")


class TestAnalysisCreate:
    def test_sm03_valid_construction(self):
        ac = AnalysisCreate(
            name="Test", location="Jakarta",
            analysis_type="business",
            data={"key": "value"}
        )
        assert ac.name == "Test"

    def test_sm04_optional_gemini_analysis_default_none(self):
        ac = AnalysisCreate(
            name="Test", location="Jakarta",
            analysis_type="business",
            data={"key": "value"}
        )
        assert ac.gemini_analysis is None


class TestUserCreate:
    def test_sm05_requires_password(self):
        uc = UserCreate(email="a@b.com", full_name="Test", password="pass123")
        assert uc.password == "pass123"

    def test_sm05b_missing_password_raises(self):
        with pytest.raises(PydanticValidationError):
            UserCreate(email="a@b.com", full_name="Test")


class TestFirebaseLogin:
    def test_sm06_valid_construction(self):
        fl = FirebaseLogin(email="a@b.com", firebase_token="tok123")
        assert fl.firebase_token == "tok123"


class TestToken:
    def test_sm07_valid_construction(self):
        t = Token(access_token="abc", token_type="bearer")
        assert t.access_token == "abc"
