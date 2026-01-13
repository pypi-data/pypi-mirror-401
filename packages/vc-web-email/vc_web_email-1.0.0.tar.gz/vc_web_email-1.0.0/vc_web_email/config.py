"""
Email configuration models.

This module defines configuration classes for different email providers
and the main EmailConfig class.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Union
from enum import Enum
from pathlib import Path
import os
import yaml
import json

from .exceptions import ConfigurationError


class EmailProvider(Enum):
    """Supported email providers."""
    SMTP = 'smtp'
    GMAIL = 'gmail'
    SENDGRID = 'sendgrid'
    AWS_SES = 'aws_ses'
    MAILGUN = 'mailgun'
    OUTLOOK = 'outlook'


@dataclass
class SMTPConfig:
    """SMTP server configuration."""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    use_tls: bool = True
    use_ssl: bool = False
    timeout: int = 30
    local_hostname: Optional[str] = None
    
    def __post_init__(self):
        if not self.host:
            raise ConfigurationError("SMTP host is required", config_key="smtp.host")
        if not self.port:
            raise ConfigurationError("SMTP port is required", config_key="smtp.port")


@dataclass
class GmailConfig:
    """Gmail configuration (uses SMTP under the hood)."""
    username: str
    password: str  # App password, not regular password
    
    def __post_init__(self):
        if not self.username:
            raise ConfigurationError("Gmail username is required", config_key="gmail.username")
        if not self.password:
            raise ConfigurationError("Gmail password (app password) is required", config_key="gmail.password")
    
    def to_smtp_config(self) -> SMTPConfig:
        """Convert to SMTP configuration."""
        return SMTPConfig(
            host='smtp.gmail.com',
            port=587,
            username=self.username,
            password=self.password,
            use_tls=True
        )


@dataclass
class SendGridConfig:
    """SendGrid configuration."""
    api_key: str
    sandbox_mode: bool = False
    
    def __post_init__(self):
        if not self.api_key:
            raise ConfigurationError("SendGrid API key is required", config_key="sendgrid.api_key")


@dataclass
class AWSSESConfig:
    """AWS SES configuration."""
    region: str
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    configuration_set: Optional[str] = None
    
    def __post_init__(self):
        if not self.region:
            raise ConfigurationError("AWS SES region is required", config_key="aws_ses.region")


@dataclass
class MailgunConfig:
    """Mailgun configuration."""
    api_key: str
    domain: str
    base_url: str = 'https://api.mailgun.net/v3'
    
    def __post_init__(self):
        if not self.api_key:
            raise ConfigurationError("Mailgun API key is required", config_key="mailgun.api_key")
        if not self.domain:
            raise ConfigurationError("Mailgun domain is required", config_key="mailgun.domain")


@dataclass
class OutlookConfig:
    """Outlook/Microsoft 365 configuration."""
    username: str
    password: str
    
    def __post_init__(self):
        if not self.username:
            raise ConfigurationError("Outlook username is required", config_key="outlook.username")
        if not self.password:
            raise ConfigurationError("Outlook password is required", config_key="outlook.password")
    
    def to_smtp_config(self) -> SMTPConfig:
        """Convert to SMTP configuration."""
        return SMTPConfig(
            host='smtp-mail.outlook.com',
            port=587,
            username=self.username,
            password=self.password,
            use_tls=True
        )


@dataclass
class EmailConfig:
    """
    Main email configuration class.
    
    Attributes:
        provider: Email provider to use
        smtp: SMTP configuration
        gmail: Gmail configuration
        sendgrid: SendGrid configuration
        aws_ses: AWS SES configuration
        mailgun: Mailgun configuration
        outlook: Outlook configuration
        default_from: Default sender email
        default_reply_to: Default reply-to address
        retry_attempts: Number of retry attempts
        retry_delay: Delay between retries (seconds)
        timeout: Connection timeout (seconds)
        debug: Enable debug mode
    """
    provider: EmailProvider
    smtp: Optional[SMTPConfig] = None
    gmail: Optional[GmailConfig] = None
    sendgrid: Optional[SendGridConfig] = None
    aws_ses: Optional[AWSSESConfig] = None
    mailgun: Optional[MailgunConfig] = None
    outlook: Optional[OutlookConfig] = None
    default_from: Optional[str] = None
    default_reply_to: Optional[str] = None
    retry_attempts: int = 3
    retry_delay: float = 1.0
    timeout: int = 30
    debug: bool = False
    
    def __post_init__(self):
        """Validate provider configuration."""
        # Convert string provider to enum
        if isinstance(self.provider, str):
            try:
                self.provider = EmailProvider(self.provider.lower())
            except ValueError:
                valid_providers = [p.value for p in EmailProvider]
                raise ConfigurationError(
                    f"Invalid provider: {self.provider}. Valid providers: {valid_providers}",
                    config_key="provider"
                )
        
        # Validate required provider config exists
        provider_config_map = {
            EmailProvider.SMTP: self.smtp,
            EmailProvider.GMAIL: self.gmail,
            EmailProvider.SENDGRID: self.sendgrid,
            EmailProvider.AWS_SES: self.aws_ses,
            EmailProvider.MAILGUN: self.mailgun,
            EmailProvider.OUTLOOK: self.outlook,
        }
        
        if provider_config_map.get(self.provider) is None:
            raise ConfigurationError(
                f"Configuration for provider '{self.provider.value}' is required",
                config_key=self.provider.value
            )
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EmailConfig':
        """
        Create configuration from dictionary.
        
        Args:
            data: Configuration dictionary
        
        Returns:
            EmailConfig instance
        """
        provider_str = data.get('provider', '').lower()
        
        # Build provider-specific configs
        smtp_config = None
        gmail_config = None
        sendgrid_config = None
        aws_ses_config = None
        mailgun_config = None
        outlook_config = None
        
        if 'smtp' in data:
            smtp_config = SMTPConfig(**data['smtp'])
        
        if 'gmail' in data:
            gmail_config = GmailConfig(**data['gmail'])
        
        if 'sendgrid' in data:
            sendgrid_config = SendGridConfig(**data['sendgrid'])
        
        if 'aws_ses' in data:
            aws_ses_config = AWSSESConfig(**data['aws_ses'])
        
        if 'mailgun' in data:
            mailgun_config = MailgunConfig(**data['mailgun'])
        
        if 'outlook' in data:
            outlook_config = OutlookConfig(**data['outlook'])
        
        return cls(
            provider=provider_str,
            smtp=smtp_config,
            gmail=gmail_config,
            sendgrid=sendgrid_config,
            aws_ses=aws_ses_config,
            mailgun=mailgun_config,
            outlook=outlook_config,
            default_from=data.get('default_from'),
            default_reply_to=data.get('default_reply_to'),
            retry_attempts=data.get('retry_attempts', 3),
            retry_delay=data.get('retry_delay', 1.0),
            timeout=data.get('timeout', 30),
            debug=data.get('debug', False)
        )
    
    @classmethod
    def from_file(cls, filepath: Union[str, Path]) -> 'EmailConfig':
        """
        Load configuration from YAML or JSON file.
        
        Args:
            filepath: Path to configuration file
        
        Returns:
            EmailConfig instance
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise ConfigurationError(f"Configuration file not found: {filepath}")
        
        try:
            with open(filepath, 'r') as f:
                if filepath.suffix in ('.yml', '.yaml'):
                    data = yaml.safe_load(f)
                elif filepath.suffix == '.json':
                    data = json.load(f)
                else:
                    raise ConfigurationError(
                        f"Unsupported config file format: {filepath.suffix}. Use .yml, .yaml, or .json"
                    )
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Error parsing YAML file: {e}")
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Error parsing JSON file: {e}")
        
        return cls.from_dict(data)
    
    @classmethod
    def from_env(cls) -> 'EmailConfig':
        """
        Load configuration from environment variables.
        
        Environment variables:
            VC_EMAIL_PROVIDER: Provider name
            VC_EMAIL_FROM: Default sender
            VC_EMAIL_SMTP_HOST, VC_EMAIL_SMTP_PORT, etc.
            VC_EMAIL_GMAIL_USERNAME, VC_EMAIL_GMAIL_PASSWORD
            VC_EMAIL_SENDGRID_API_KEY
            etc.
        
        Returns:
            EmailConfig instance
        """
        provider = os.getenv('VC_EMAIL_PROVIDER', 'smtp').lower()
        
        config_data = {
            'provider': provider,
            'default_from': os.getenv('VC_EMAIL_FROM'),
            'default_reply_to': os.getenv('VC_EMAIL_REPLY_TO'),
            'retry_attempts': int(os.getenv('VC_EMAIL_RETRY_ATTEMPTS', '3')),
            'timeout': int(os.getenv('VC_EMAIL_TIMEOUT', '30')),
            'debug': os.getenv('VC_EMAIL_DEBUG', '').lower() in ('true', '1', 'yes'),
        }
        
        # SMTP config
        if os.getenv('VC_EMAIL_SMTP_HOST'):
            config_data['smtp'] = {
                'host': os.getenv('VC_EMAIL_SMTP_HOST'),
                'port': int(os.getenv('VC_EMAIL_SMTP_PORT', '587')),
                'username': os.getenv('VC_EMAIL_SMTP_USERNAME'),
                'password': os.getenv('VC_EMAIL_SMTP_PASSWORD'),
                'use_tls': os.getenv('VC_EMAIL_SMTP_TLS', 'true').lower() in ('true', '1', 'yes'),
            }
        
        # Gmail config
        if os.getenv('VC_EMAIL_GMAIL_USERNAME'):
            config_data['gmail'] = {
                'username': os.getenv('VC_EMAIL_GMAIL_USERNAME'),
                'password': os.getenv('VC_EMAIL_GMAIL_PASSWORD'),
            }
        
        # SendGrid config
        if os.getenv('VC_EMAIL_SENDGRID_API_KEY'):
            config_data['sendgrid'] = {
                'api_key': os.getenv('VC_EMAIL_SENDGRID_API_KEY'),
            }
        
        # AWS SES config
        if os.getenv('VC_EMAIL_AWS_SES_REGION'):
            config_data['aws_ses'] = {
                'region': os.getenv('VC_EMAIL_AWS_SES_REGION'),
                'access_key_id': os.getenv('VC_EMAIL_AWS_ACCESS_KEY_ID'),
                'secret_access_key': os.getenv('VC_EMAIL_AWS_SECRET_ACCESS_KEY'),
            }
        
        # Mailgun config
        if os.getenv('VC_EMAIL_MAILGUN_API_KEY'):
            config_data['mailgun'] = {
                'api_key': os.getenv('VC_EMAIL_MAILGUN_API_KEY'),
                'domain': os.getenv('VC_EMAIL_MAILGUN_DOMAIN'),
            }
        
        # Outlook config
        if os.getenv('VC_EMAIL_OUTLOOK_USERNAME'):
            config_data['outlook'] = {
                'username': os.getenv('VC_EMAIL_OUTLOOK_USERNAME'),
                'password': os.getenv('VC_EMAIL_OUTLOOK_PASSWORD'),
            }
        
        return cls.from_dict(config_data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        result = {
            'provider': self.provider.value,
            'default_from': self.default_from,
            'default_reply_to': self.default_reply_to,
            'retry_attempts': self.retry_attempts,
            'retry_delay': self.retry_delay,
            'timeout': self.timeout,
            'debug': self.debug,
        }
        
        # Add provider-specific config without sensitive data
        if self.smtp:
            result['smtp'] = {
                'host': self.smtp.host,
                'port': self.smtp.port,
                'use_tls': self.smtp.use_tls,
            }
        
        return result
