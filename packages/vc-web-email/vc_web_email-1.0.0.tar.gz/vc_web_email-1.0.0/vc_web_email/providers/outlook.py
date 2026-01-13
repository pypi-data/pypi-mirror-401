"""
Outlook email provider.

This module implements the Outlook/Microsoft 365 email provider
which uses SMTP with Outlook-specific configuration.
"""

from .smtp import SMTPProvider
from ..config import EmailConfig, SMTPConfig


class OutlookProvider(SMTPProvider):
    """
    Outlook/Microsoft 365 email provider.
    
    Sends emails through Outlook's SMTP server.
    """
    
    def __init__(self, config: EmailConfig):
        """
        Initialize Outlook provider.
        
        Args:
            config: Email configuration with outlook settings
        """
        # Convert Outlook config to SMTP config
        outlook_smtp = SMTPConfig(
            host='smtp-mail.outlook.com',
            port=587,
            username=config.outlook.username,
            password=config.outlook.password,
            use_tls=True,
            use_ssl=False,
            timeout=config.timeout
        )
        
        super().__init__(config, outlook_smtp)
    
    @property
    def name(self) -> str:
        return 'outlook'
