"""
Tests for custom exceptions.
"""

import pytest
from vc_web_email.exceptions import (
    VCEmailError, ConfigurationError, ValidationError,
    ProviderError, ConnectionError, AuthenticationError,
    RateLimitError, AttachmentError, TemplateError, RetryError
)


class TestVCEmailError:
    """Tests for base exception."""
    
    def test_create_with_message(self):
        error = VCEmailError("Test error")
        assert str(error) == "Test error"
    
    def test_create_with_details(self):
        error = VCEmailError("Test error", details={'key': 'value'})
        assert error.details == {'key': 'value'}
        assert 'key' in str(error)


class TestConfigurationError:
    """Tests for ConfigurationError."""
    
    def test_create_with_config_key(self):
        error = ConfigurationError("Invalid config", config_key="smtp.host")
        assert error.config_key == "smtp.host"
    
    def test_error_message(self):
        error = ConfigurationError("Missing required field")
        assert "Missing required field" in str(error)


class TestValidationError:
    """Tests for ValidationError."""
    
    def test_create_with_field(self):
        error = ValidationError("Invalid email", field="to")
        assert error.field == "to"
    
    def test_error_message(self):
        error = ValidationError("Subject is required", field="subject")
        assert "Subject is required" in str(error)


class TestProviderError:
    """Tests for ProviderError."""
    
    def test_create_with_provider_and_status(self):
        error = ProviderError("API error", provider="sendgrid", status_code=401)
        assert error.provider == "sendgrid"
        assert error.status_code == 401


class TestConnectionError:
    """Tests for ConnectionError."""
    
    def test_create_with_host_and_port(self):
        error = ConnectionError("Connection failed", host="smtp.example.com", port=587)
        assert error.host == "smtp.example.com"
        assert error.port == 587


class TestAuthenticationError:
    """Tests for AuthenticationError."""
    
    def test_create_with_provider(self):
        error = AuthenticationError("Login failed", provider="gmail")
        assert error.provider == "gmail"


class TestRateLimitError:
    """Tests for RateLimitError."""
    
    def test_create_with_retry_after(self):
        error = RateLimitError("Rate limit exceeded", retry_after=60)
        assert error.retry_after == 60


class TestAttachmentError:
    """Tests for AttachmentError."""
    
    def test_create_with_filename(self):
        error = AttachmentError("File too large", filename="big_file.pdf")
        assert error.filename == "big_file.pdf"


class TestRetryError:
    """Tests for RetryError."""
    
    def test_create_with_attempts(self):
        last_error = Exception("Final error")
        error = RetryError("All retries failed", attempts=3, last_error=last_error)
        assert error.attempts == 3
        assert error.last_error == last_error
