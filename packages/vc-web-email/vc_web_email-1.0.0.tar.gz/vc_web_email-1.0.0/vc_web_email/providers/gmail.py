"""
Gmail email provider.

This module implements the Gmail email provider which uses SMTP
with Gmail-specific configuration.
"""

from typing import Optional
from .smtp import SMTPProvider
from ..config import EmailConfig, SMTPConfig


class GmailProvider(SMTPProvider):
    """
    Gmail email provider.
    
    Sends emails through Gmail's SMTP server.
    Uses OAuth or App Passwords for authentication.
    """
    
    def __init__(self, config: EmailConfig):
        """
        Initialize Gmail provider.
        
        Args:
            config: Email configuration with gmail settings
        """
        # Convert Gmail config to SMTP config
        gmail_smtp = SMTPConfig(
            host='smtp.gmail.com',
            port=587,
            username=config.gmail.username,
            password=config.gmail.password,
            use_tls=True,
            use_ssl=False,
            timeout=config.timeout
        )
        
        super().__init__(config, gmail_smtp)
    
    @property
    def name(self) -> str:
        return 'gmail'
