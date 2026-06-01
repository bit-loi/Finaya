"""
TDD Tests: Custom Exceptions
Scenarios: EX-01 through EX-09
"""
import pytest
from app.core.exceptions import (
    FinayaException, AuthenticationError, AuthorizationError,
    ValidationError, NotFoundError, DatabaseError, ExternalServiceError,
)


class TestExceptionStatusCodes:
    def test_ex01_finaya_exception_default_500(self):
        exc = FinayaException("test error")
        assert exc.status_code == 500
        assert exc.message == "test error"

    def test_ex02_authentication_error_401(self):
        assert AuthenticationError().status_code == 401

    def test_ex03_authorization_error_403(self):
        assert AuthorizationError().status_code == 403

    def test_ex04_validation_error_422(self):
        assert ValidationError().status_code == 422

    def test_ex05_not_found_error_404(self):
        assert NotFoundError().status_code == 404

    def test_ex06_database_error_500(self):
        assert DatabaseError().status_code == 500

    def test_ex07_external_service_error_502(self):
        assert ExternalServiceError().status_code == 502


class TestExceptionInheritance:
    def test_ex08_all_inherit_from_finaya_exception(self):
        assert isinstance(AuthenticationError(), FinayaException)
        assert isinstance(AuthorizationError(), FinayaException)
        assert isinstance(ValidationError(), FinayaException)
        assert isinstance(NotFoundError(), FinayaException)
        assert isinstance(DatabaseError(), FinayaException)
        assert isinstance(ExternalServiceError(), FinayaException)


class TestExceptionCustomMessage:
    def test_ex09_custom_message_stored(self):
        exc = AuthenticationError("custom msg")
        assert exc.message == "custom msg"
        assert str(exc) == "custom msg"

    def test_ex09b_default_messages(self):
        assert AuthenticationError().message == "Authentication failed"
        assert ValidationError().message == "Validation failed"
        assert NotFoundError().message == "Resource not found"
        assert DatabaseError().message == "Database operation failed"
