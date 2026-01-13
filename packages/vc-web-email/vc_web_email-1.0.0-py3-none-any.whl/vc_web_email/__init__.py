"""
vc_web_email - A Unified Email Library for VentureCube Organization
====================================================================

A powerful, provider-agnostic email library supporting multiple email 
providers including SMTP, Gmail, SendGrid, AWS SES, and Mailgun.

Basic usage:
    >>> from vc_web_email import EmailClient
    >>> client = EmailClient.from_config('config.yml')
    >>> response = client.send(
    ...     to='recipient@example.com',
    ...     subject='Hello',
    ...     text='Hello from vc_web_email!'
    ... )
"""

__version__ = '1.0.0'
__author__ = 'VentureCube'
__email__ = 'support@venturecube.com'

from .client import EmailClient
from .message import EmailMessage, Attachment
from .config import EmailConfig
from .response import EmailResponse
from .exceptions import (
    VCEmailError,
    ConfigurationError,
    ValidationError,
    ProviderError,
    ConnectionError,
    AuthenticationError,
    RateLimitError,
    AttachmentError
)

__all__ = [
    # Version
    '__version__',
    
    # Main classes
    'EmailClient',
    'EmailMessage',
    'Attachment',
    'EmailConfig',
    'EmailResponse',
    
    # Exceptions
    'VCEmailError',
    'ConfigurationError',
    'ValidationError',
    'ProviderError',
    'ConnectionError',
    'AuthenticationError',
    'RateLimitError',
    'AttachmentError'
]
