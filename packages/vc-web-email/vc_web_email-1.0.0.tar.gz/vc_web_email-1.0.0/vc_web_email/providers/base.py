"""
Base email provider class.

This module defines the abstract base class for all email providers.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..config import EmailConfig
from ..message import EmailMessage
from ..response import EmailResponse, BulkEmailResponse


class BaseEmailProvider(ABC):
    """
    Abstract base class for email providers.
    
    All email provider implementations must inherit from this class
    and implement the required methods.
    """
    
    def __init__(self, config: EmailConfig):
        """
        Initialize the provider.
        
        Args:
            config: Email configuration
        """
        self.config = config
        self._connection = None
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name."""
        pass
    
    @abstractmethod
    def send(self, message: EmailMessage) -> EmailResponse:
        """
        Send a single email.
        
        Args:
            message: Email message to send
        
        Returns:
            EmailResponse with send result
        """
        pass
    
    def send_bulk(self, messages: List[EmailMessage]) -> BulkEmailResponse:
        """
        Send multiple emails.
        
        Default implementation sends emails one by one.
        Providers can override for batch sending if supported.
        
        Args:
            messages: List of email messages to send
        
        Returns:
            BulkEmailResponse with results for all emails
        """
        responses = []
        successful = 0
        failed = 0
        
        for message in messages:
            try:
                response = self.send(message)
                responses.append(response)
                if response.success:
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                response = EmailResponse.failure_response(
                    error=str(e),
                    provider=self.name,
                    recipients=message.get_all_recipients()
                )
                responses.append(response)
                failed += 1
        
        return BulkEmailResponse(
            total=len(messages),
            successful=successful,
            failed=failed,
            responses=responses
        )
    
    def connect(self) -> None:
        """
        Establish connection to the email service.
        
        Override in providers that need persistent connections.
        """
        pass
    
    def disconnect(self) -> None:
        """
        Close connection to the email service.
        
        Override in providers that need persistent connections.
        """
        pass
    
    def is_connected(self) -> bool:
        """
        Check if connected to the email service.
        
        Returns:
            True if connected, False otherwise
        """
        return self._connection is not None
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
        return False
    
    def _get_from_address(self, message: EmailMessage) -> str:
        """
        Get the from address for a message.
        
        Args:
            message: Email message
        
        Returns:
            From email address
        """
        return message.from_email or self.config.default_from or ''
    
    def _get_reply_to(self, message: EmailMessage) -> Optional[str]:
        """
        Get the reply-to address for a message.
        
        Args:
            message: Email message
        
        Returns:
            Reply-to email address or None
        """
        return message.reply_to or self.config.default_reply_to
