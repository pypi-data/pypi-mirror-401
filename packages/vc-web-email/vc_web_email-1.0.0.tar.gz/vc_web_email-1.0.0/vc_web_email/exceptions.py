"""
Custom exceptions for vc_web_email library.

This module defines all exception classes used throughout the library
to provide clear and specific error handling.
"""

from typing import Optional, Dict, Any


class VCEmailError(Exception):
    """Base exception for all vc_web_email errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message


class ConfigurationError(VCEmailError):
    """Raised when there's an error in the email configuration."""
    
    def __init__(self, message: str, config_key: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.config_key = config_key
        super().__init__(message, details)


class ValidationError(VCEmailError):
    """Raised when email message validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.field = field
        super().__init__(message, details)


class ProviderError(VCEmailError):
    """Raised when there's an error with the email provider."""
    
    def __init__(self, message: str, provider: Optional[str] = None, 
                 status_code: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        self.provider = provider
        self.status_code = status_code
        super().__init__(message, details)


class ConnectionError(VCEmailError):
    """Raised when connection to email server fails."""
    
    def __init__(self, message: str, host: Optional[str] = None, 
                 port: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        self.host = host
        self.port = port
        super().__init__(message, details)


class AuthenticationError(VCEmailError):
    """Raised when authentication with email provider fails."""
    
    def __init__(self, message: str, provider: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.provider = provider
        super().__init__(message, details)


class RateLimitError(VCEmailError):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str, retry_after: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        self.retry_after = retry_after
        super().__init__(message, details)


class AttachmentError(VCEmailError):
    """Raised when there's an error with email attachments."""
    
    def __init__(self, message: str, filename: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.filename = filename
        super().__init__(message, details)


class TemplateError(VCEmailError):
    """Raised when there's an error with email templates."""
    
    def __init__(self, message: str, template_name: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.template_name = template_name
        super().__init__(message, details)


class RetryError(VCEmailError):
    """Raised when all retry attempts have been exhausted."""
    
    def __init__(self, message: str, attempts: int = 0, last_error: Optional[Exception] = None, 
                 details: Optional[Dict[str, Any]] = None):
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(message, details)
