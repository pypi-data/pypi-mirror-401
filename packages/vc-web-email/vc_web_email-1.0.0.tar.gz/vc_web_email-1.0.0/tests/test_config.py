"""
Tests for EmailConfig.

This module contains unit tests for the EmailConfig class.
"""

import pytest
import tempfile
from pathlib import Path
import os

from vc_web_email import EmailConfig
from vc_web_email.config import EmailProvider, SMTPConfig, GmailConfig
from vc_web_email.exceptions import ConfigurationError


class TestEmailConfig:
    """Tests for EmailConfig class."""
    
    def test_create_smtp_config(self):
        """Test creating SMTP configuration."""
        config = EmailConfig(
            provider=EmailProvider.SMTP,
            smtp=SMTPConfig(
                host='smtp.example.com',
                port=587,
                username='user@example.com',
                password='password'
            ),
            default_from='user@example.com'
        )
        
        assert config.provider == EmailProvider.SMTP
        assert config.smtp.host == 'smtp.example.com'
        assert config.smtp.port == 587
    
    def test_create_config_with_string_provider(self):
        """Test creating config with string provider."""
        config = EmailConfig(
            provider='smtp',
            smtp=SMTPConfig(
                host='smtp.example.com',
                port=587
            )
        )
        
        assert config.provider == EmailProvider.SMTP
    
    def test_invalid_provider_string(self):
        """Test invalid provider string raises error."""
        with pytest.raises(ConfigurationError) as exc_info:
            EmailConfig(provider='invalid')
        
        assert 'Invalid provider' in str(exc_info.value)
    
    def test_missing_provider_config(self):
        """Test missing provider-specific config raises error."""
        with pytest.raises(ConfigurationError):
            EmailConfig(
                provider=EmailProvider.SMTP,
                # Missing smtp config
            )
    
    def test_from_dict_smtp(self):
        """Test creating config from dictionary."""
        data = {
            'provider': 'smtp',
            'smtp': {
                'host': 'smtp.example.com',
                'port': 587,
                'username': 'user@example.com',
                'password': 'password'
            },
            'default_from': 'user@example.com',
            'retry_attempts': 5
        }
        
        config = EmailConfig.from_dict(data)
        
        assert config.provider == EmailProvider.SMTP
        assert config.smtp.host == 'smtp.example.com'
        assert config.retry_attempts == 5
    
    def test_from_dict_gmail(self):
        """Test creating Gmail config from dictionary."""
        data = {
            'provider': 'gmail',
            'gmail': {
                'username': 'test@gmail.com',
                'password': 'app-password'
            },
            'default_from': 'test@gmail.com'
        }
        
        config = EmailConfig.from_dict(data)
        
        assert config.provider == EmailProvider.GMAIL
        assert config.gmail.username == 'test@gmail.com'
    
    def test_from_dict_sendgrid(self):
        """Test creating SendGrid config from dictionary."""
        data = {
            'provider': 'sendgrid',
            'sendgrid': {
                'api_key': 'SG.test-key'
            },
            'default_from': 'test@example.com'
        }
        
        config = EmailConfig.from_dict(data)
        
        assert config.provider == EmailProvider.SENDGRID
        assert config.sendgrid.api_key == 'SG.test-key'
    
    def test_from_yaml_file(self, tmp_path):
        """Test loading config from YAML file."""
        config_file = tmp_path / "config.yml"
        config_content = """
provider: smtp
smtp:
  host: smtp.example.com
  port: 587
  username: test@example.com
  password: secretpassword
default_from: test@example.com
retry_attempts: 3
timeout: 30
debug: true
"""
        config_file.write_text(config_content)
        
        config = EmailConfig.from_file(config_file)
        
        assert config.provider == EmailProvider.SMTP
        assert config.smtp.host == 'smtp.example.com'
        assert config.retry_attempts == 3
        assert config.debug is True
    
    def test_from_json_file(self, tmp_path):
        """Test loading config from JSON file."""
        import json
        
        config_file = tmp_path / "config.json"
        config_data = {
            'provider': 'gmail',
            'gmail': {
                'username': 'test@gmail.com',
                'password': 'app-password'
            },
            'default_from': 'test@gmail.com'
        }
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        config = EmailConfig.from_file(config_file)
        
        assert config.provider == EmailProvider.GMAIL
    
    def test_from_nonexistent_file(self):
        """Test loading from non-existent file raises error."""
        with pytest.raises(ConfigurationError):
            EmailConfig.from_file('/nonexistent/config.yml')
    
    def test_from_unsupported_file_format(self, tmp_path):
        """Test loading from unsupported file format raises error."""
        config_file = tmp_path / "config.xml"
        config_file.write_text("<config></config>")
        
        with pytest.raises(ConfigurationError) as exc_info:
            EmailConfig.from_file(config_file)
        
        assert 'Unsupported' in str(exc_info.value)
    
    def test_to_dict(self):
        """Test converting config to dictionary."""
        config = EmailConfig(
            provider=EmailProvider.SMTP,
            smtp=SMTPConfig(
                host='smtp.example.com',
                port=587
            ),
            default_from='test@example.com',
            retry_attempts=5
        )
        
        result = config.to_dict()
        
        assert result['provider'] == 'smtp'
        assert result['smtp']['host'] == 'smtp.example.com'
        assert result['retry_attempts'] == 5
    
    def test_default_values(self):
        """Test default configuration values."""
        config = EmailConfig(
            provider=EmailProvider.SMTP,
            smtp=SMTPConfig(
                host='smtp.example.com',
                port=587
            )
        )
        
        assert config.retry_attempts == 3
        assert config.retry_delay == 1.0
        assert config.timeout == 30
        assert config.debug is False


class TestFromEnv:
    """Tests for EmailConfig.from_env."""
    
    def test_from_env_smtp(self, monkeypatch):
        """Test loading SMTP config from environment."""
        monkeypatch.setenv('VC_EMAIL_PROVIDER', 'smtp')
        monkeypatch.setenv('VC_EMAIL_FROM', 'test@example.com')
        monkeypatch.setenv('VC_EMAIL_SMTP_HOST', 'smtp.example.com')
        monkeypatch.setenv('VC_EMAIL_SMTP_PORT', '587')
        monkeypatch.setenv('VC_EMAIL_SMTP_USERNAME', 'user@example.com')
        monkeypatch.setenv('VC_EMAIL_SMTP_PASSWORD', 'password123')
        
        config = EmailConfig.from_env()
        
        assert config.provider == EmailProvider.SMTP
        assert config.default_from == 'test@example.com'
        assert config.smtp.host == 'smtp.example.com'
        assert config.smtp.port == 587
    
    def test_from_env_gmail(self, monkeypatch):
        """Test loading Gmail config from environment."""
        monkeypatch.setenv('VC_EMAIL_PROVIDER', 'gmail')
        monkeypatch.setenv('VC_EMAIL_GMAIL_USERNAME', 'test@gmail.com')
        monkeypatch.setenv('VC_EMAIL_GMAIL_PASSWORD', 'app-password')
        
        config = EmailConfig.from_env()
        
        assert config.provider == EmailProvider.GMAIL
        assert config.gmail.username == 'test@gmail.com'
    
    def test_from_env_sendgrid(self, monkeypatch):
        """Test loading SendGrid config from environment."""
        monkeypatch.setenv('VC_EMAIL_PROVIDER', 'sendgrid')
        monkeypatch.setenv('VC_EMAIL_SENDGRID_API_KEY', 'SG.test-key')
        monkeypatch.setenv('VC_EMAIL_FROM', 'test@example.com')
        
        config = EmailConfig.from_env()
        
        assert config.provider == EmailProvider.SENDGRID
        assert config.sendgrid.api_key == 'SG.test-key'
    
    def test_from_env_debug_mode(self, monkeypatch):
        """Test debug mode from environment."""
        monkeypatch.setenv('VC_EMAIL_PROVIDER', 'smtp')
        monkeypatch.setenv('VC_EMAIL_SMTP_HOST', 'smtp.example.com')
        monkeypatch.setenv('VC_EMAIL_SMTP_PORT', '587')
        monkeypatch.setenv('VC_EMAIL_DEBUG', 'true')
        
        config = EmailConfig.from_env()
        
        assert config.debug is True


class TestSMTPConfig:
    """Tests for SMTPConfig."""
    
    def test_create_smtp_config(self):
        """Test creating SMTP config."""
        config = SMTPConfig(
            host='smtp.example.com',
            port=587,
            username='user',
            password='pass',
            use_tls=True
        )
        
        assert config.host == 'smtp.example.com'
        assert config.port == 587
        assert config.use_tls is True
    
    def test_missing_host_raises_error(self):
        """Test missing host raises error."""
        with pytest.raises(ConfigurationError):
            SMTPConfig(host='', port=587)
    
    def test_missing_port_raises_error(self):
        """Test missing port raises error."""
        with pytest.raises(ConfigurationError):
            SMTPConfig(host='smtp.example.com', port=0)
    
    def test_default_values(self):
        """Test default SMTP config values."""
        config = SMTPConfig(host='smtp.example.com', port=587)
        
        assert config.use_tls is True
        assert config.use_ssl is False
        assert config.timeout == 30


class TestGmailConfig:
    """Tests for GmailConfig."""
    
    def test_create_gmail_config(self):
        """Test creating Gmail config."""
        config = GmailConfig(
            username='test@gmail.com',
            password='app-password'
        )
        
        assert config.username == 'test@gmail.com'
        assert config.password == 'app-password'
    
    def test_to_smtp_config(self):
        """Test converting Gmail config to SMTP."""
        gmail_config = GmailConfig(
            username='test@gmail.com',
            password='app-password'
        )
        
        smtp_config = gmail_config.to_smtp_config()
        
        assert smtp_config.host == 'smtp.gmail.com'
        assert smtp_config.port == 587
        assert smtp_config.username == 'test@gmail.com'
        assert smtp_config.use_tls is True
    
    def test_missing_username_raises_error(self):
        """Test missing username raises error."""
        with pytest.raises(ConfigurationError):
            GmailConfig(username='', password='password')
    
    def test_missing_password_raises_error(self):
        """Test missing password raises error."""
        with pytest.raises(ConfigurationError):
            GmailConfig(username='test@gmail.com', password='')
