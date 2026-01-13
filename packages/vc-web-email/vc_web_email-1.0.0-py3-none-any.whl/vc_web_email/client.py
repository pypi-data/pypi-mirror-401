"""
Main EmailClient class.

This module provides the main EmailClient class that serves as the
unified interface for sending emails through various providers.
"""

import time
from typing import Dict, List, Optional, Union, Any
from pathlib import Path

from .config import EmailConfig, EmailProvider
from .message import EmailMessage, Attachment
from .response import EmailResponse, BulkEmailResponse
from .exceptions import (
    VCEmailError, ConfigurationError, ValidationError,
    ProviderError, RetryError
)
from .utils.validator import EmailValidator
from .utils.logger import EmailLogger
from .providers.base import BaseEmailProvider
from .providers.smtp import SMTPProvider
from .providers.gmail import GmailProvider
from .providers.sendgrid import SendGridProvider
from .providers.aws_ses import AWSSESProvider
from .providers.mailgun import MailgunProvider
from .providers.outlook import OutlookProvider


class EmailClient:
    """
    Unified email client for sending emails through various providers.
    
    This class provides a simple, unified API for sending emails
    regardless of the underlying email provider.
    
    Example:
        >>> client = EmailClient.from_config('email-config.yml')
        >>> response = client.send(
        ...     to='recipient@example.com',
        ...     subject='Hello',
        ...     text='Hello World!'
        ... )
        >>> print(response.success)
        True
    """
    
    # Provider class mapping
    PROVIDER_MAP = {
        EmailProvider.SMTP: SMTPProvider,
        EmailProvider.GMAIL: GmailProvider,
        EmailProvider.SENDGRID: SendGridProvider,
        EmailProvider.AWS_SES: AWSSESProvider,
        EmailProvider.MAILGUN: MailgunProvider,
        EmailProvider.OUTLOOK: OutlookProvider,
    }
    
    def __init__(self, config: Union[Dict[str, Any], EmailConfig]):
        """
        Initialize the email client.
        
        Args:
            config: Configuration dictionary or EmailConfig object
        
        Raises:
            ConfigurationError: If configuration is invalid
        """
        if isinstance(config, dict):
            self.config = EmailConfig.from_dict(config)
        else:
            self.config = config
        
        # Initialize logger
        EmailLogger.set_debug(self.config.debug)
        self._logger = EmailLogger.get_logger(debug=self.config.debug)
        
        # Initialize provider
        self._provider = self._create_provider()
        
        self._logger.debug(f"EmailClient initialized with provider: {self.config.provider.value}")
    
    def _create_provider(self) -> BaseEmailProvider:
        """Create the appropriate provider instance."""
        provider_class = self.PROVIDER_MAP.get(self.config.provider)
        
        if not provider_class:
            raise ConfigurationError(
                f"Unsupported provider: {self.config.provider.value}",
                config_key="provider"
            )
        
        return provider_class(self.config)
    
    @classmethod
    def from_config(cls, filepath: Union[str, Path]) -> 'EmailClient':
        """
        Create an EmailClient from a configuration file.
        
        Args:
            filepath: Path to YAML or JSON configuration file
        
        Returns:
            Configured EmailClient instance
        
        Example:
            >>> client = EmailClient.from_config('email-config.yml')
        """
        config = EmailConfig.from_file(filepath)
        return cls(config)
    
    @classmethod
    def from_env(cls) -> 'EmailClient':
        """
        Create an EmailClient from environment variables.
        
        Returns:
            Configured EmailClient instance
        
        Example:
            >>> client = EmailClient.from_env()
        """
        config = EmailConfig.from_env()
        return cls(config)
    
    def send(self,
             to: Union[str, List[str]],
             subject: str,
             text: Optional[str] = None,
             html: Optional[str] = None,
             from_email: Optional[str] = None,
             cc: Optional[Union[str, List[str]]] = None,
             bcc: Optional[Union[str, List[str]]] = None,
             reply_to: Optional[str] = None,
             attachments: Optional[List[Union[Attachment, str, Path]]] = None,
             headers: Optional[Dict[str, str]] = None,
             tags: Optional[List[str]] = None,
             metadata: Optional[Dict[str, Any]] = None,
             validate: bool = True) -> EmailResponse:
        """
        Send an email.
        
        Args:
            to: Recipient email address(es)
            subject: Email subject
            text: Plain text body
            html: HTML body
            from_email: Sender email (overrides default)
            cc: CC recipients
            bcc: BCC recipients
            reply_to: Reply-to address
            attachments: List of attachments
            headers: Custom email headers
            tags: Tags for tracking
            metadata: Additional metadata
            validate: Whether to validate the message
        
        Returns:
            EmailResponse with send result
        
        Example:
            >>> response = client.send(
            ...     to='recipient@example.com',
            ...     subject='Hello',
            ...     text='Hello World!',
            ...     html='<h1>Hello World!</h1>'
            ... )
        """
        # Build message
        message = EmailMessage(
            to=to,
            subject=subject,
            text=text,
            html=html,
            from_email=from_email,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            headers=headers or {},
            tags=tags or [],
            metadata=metadata or {}
        )
        
        # Add attachments
        if attachments:
            for attachment in attachments:
                message.add_attachment(attachment)
        
        return self.send_message(message, validate=validate)
    
    def send_message(self, message: EmailMessage, validate: bool = True) -> EmailResponse:
        """
        Send an email message.
        
        Args:
            message: EmailMessage to send
            validate: Whether to validate the message
        
        Returns:
            EmailResponse with send result
        """
        # Validate message
        if validate:
            try:
                EmailValidator.validate_message(message)
            except ValidationError as e:
                return EmailResponse.failure_response(
                    error=str(e),
                    provider=self._provider.name,
                    recipients=message.get_all_recipients()
                )
        
        # Send with retry logic
        return self._send_with_retry(message)
    
    def _send_with_retry(self, message: EmailMessage) -> EmailResponse:
        """
        Send email with retry logic.
        
        Args:
            message: EmailMessage to send
        
        Returns:
            EmailResponse with send result
        """
        last_error = None
        recipients = message.get_all_recipients()
        
        for attempt in range(self.config.retry_attempts):
            try:
                self._logger.debug(f"Sending email (attempt {attempt + 1}/{self.config.retry_attempts})")
                
                response = self._provider.send(message)
                
                if response.success:
                    self._logger.info(
                        f"Email sent successfully to {', '.join(recipients[:3])}{'...' if len(recipients) > 3 else ''}"
                    )
                    return response
                
                last_error = response.error
                self._logger.warning(f"Send attempt {attempt + 1} failed: {response.error}")
                
            except Exception as e:
                last_error = str(e)
                self._logger.warning(f"Send attempt {attempt + 1} raised exception: {e}")
            
            # Wait before retry (if not last attempt)
            if attempt < self.config.retry_attempts - 1:
                wait_time = self.config.retry_delay * (2 ** attempt)  # Exponential backoff
                self._logger.debug(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
        
        # All retries exhausted
        self._logger.error(f"Email send failed after {self.config.retry_attempts} attempts: {last_error}")
        
        return EmailResponse.failure_response(
            error=f"Failed after {self.config.retry_attempts} attempts. Last error: {last_error}",
            provider=self._provider.name,
            recipients=recipients
        )
    
    def send_bulk(self, messages: List[EmailMessage], 
                  validate: bool = True) -> BulkEmailResponse:
        """
        Send multiple emails.
        
        Args:
            messages: List of EmailMessage objects
            validate: Whether to validate messages
        
        Returns:
            BulkEmailResponse with results for all emails
        """
        if validate:
            for message in messages:
                try:
                    EmailValidator.validate_message(message)
                except ValidationError as e:
                    self._logger.error(f"Validation failed for message to {message.to}: {e}")
                    # Continue with other messages
        
        self._logger.info(f"Sending bulk email to {len(messages)} recipients")
        
        response = self._provider.send_bulk(messages)
        
        self._logger.info(
            f"Bulk send complete: {response.successful}/{response.total} successful"
        )
        
        return response
    
    def send_template(self,
                      to: Union[str, List[str]],
                      template_id: str,
                      template_data: Dict[str, Any],
                      subject: Optional[str] = None,
                      from_email: Optional[str] = None,
                      **kwargs) -> EmailResponse:
        """
        Send an email using a provider template.
        
        Args:
            to: Recipient email address(es)
            template_id: Provider template ID
            template_data: Data for template substitution
            subject: Optional subject override
            from_email: Sender email
            **kwargs: Additional message options
        
        Returns:
            EmailResponse with send result
        """
        message = EmailMessage(
            to=to,
            subject=subject or '',
            template_id=template_id,
            template_data=template_data,
            from_email=from_email,
            **kwargs
        )
        
        return self.send_message(message)
    
    def test_connection(self) -> bool:
        """
        Test the connection to the email provider.
        
        Returns:
            True if connection is successful
        """
        try:
            self._provider.connect()
            self._provider.disconnect()
            return True
        except Exception as e:
            self._logger.error(f"Connection test failed: {e}")
            return False
    
    def get_provider_name(self) -> str:
        """Get the name of the current provider."""
        return self._provider.name
    
    def __enter__(self):
        """Context manager entry."""
        self._provider.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self._provider.disconnect()
        return False
    
    def close(self) -> None:
        """Close the client and disconnect from provider."""
        self._provider.disconnect()
