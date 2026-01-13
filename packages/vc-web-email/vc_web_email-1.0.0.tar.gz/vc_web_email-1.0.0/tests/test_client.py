"""
Tests for EmailClient.

This module contains unit tests for the main EmailClient class.
"""

import pytest
import os
import tempfile
from pathlib import Path

from vc_web_email import EmailClient, EmailMessage, EmailConfig
from vc_web_email.exceptions import ConfigurationError, ValidationError


class TestEmailClientInit:
    """Tests for EmailClient initialization."""
    
    def test_init_with_dict(self):
        """Test initialization with dictionary config."""
        config = {
            'provider': 'smtp',
            'smtp': {
                'host': 'smtp.example.com',
                'port': 587,
                'username': 'test@example.com',
                'password': 'password123',
            },
            'default_from': 'test@example.com'
        }
        
        client = EmailClient(config)
        
        assert client.config.provider.value == 'smtp'
        assert client.config.smtp.host == 'smtp.example.com'
        assert client.config.smtp.port == 587
        assert client.config.default_from == 'test@example.com'
    
    def test_init_with_gmail_config(self):
        """Test initialization with Gmail configuration."""
        config = {
            'provider': 'gmail',
            'gmail': {
                'username': 'test@gmail.com',
                'password': 'app-password-here',
            },
            'default_from': 'test@gmail.com'
        }
        
        client = EmailClient(config)
        
        assert client.config.provider.value == 'gmail'
        assert client.get_provider_name() == 'gmail'
    
    def test_init_with_sendgrid_config(self):
        """Test initialization with SendGrid configuration."""
        config = {
            'provider': 'sendgrid',
            'sendgrid': {
                'api_key': 'SG.test-api-key-here',
            },
            'default_from': 'test@example.com'
        }
        
        client = EmailClient(config)
        
        assert client.config.provider.value == 'sendgrid'
        assert client.get_provider_name() == 'sendgrid'
    
    def test_init_with_aws_ses_config(self):
        """Test initialization with AWS SES configuration."""
        config = {
            'provider': 'aws_ses',
            'aws_ses': {
                'region': 'us-east-1',
                'access_key_id': 'AKIAIOSFODNN7EXAMPLE',
                'secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
            },
            'default_from': 'test@example.com'
        }
        
        client = EmailClient(config)
        
        assert client.config.provider.value == 'aws_ses'
        assert client.get_provider_name() == 'aws_ses'
    
    def test_init_with_mailgun_config(self):
        """Test initialization with Mailgun configuration."""
        config = {
            'provider': 'mailgun',
            'mailgun': {
                'api_key': 'key-xxx',
                'domain': 'mg.example.com',
            },
            'default_from': 'test@mg.example.com'
        }
        
        client = EmailClient(config)
        
        assert client.config.provider.value == 'mailgun'
        assert client.get_provider_name() == 'mailgun'
    
    def test_init_with_outlook_config(self):
        """Test initialization with Outlook configuration."""
        config = {
            'provider': 'outlook',
            'outlook': {
                'username': 'test@outlook.com',
                'password': 'password123',
            },
            'default_from': 'test@outlook.com'
        }
        
        client = EmailClient(config)
        
        assert client.config.provider.value == 'outlook'
        assert client.get_provider_name() == 'outlook'
    
    def test_init_invalid_provider(self):
        """Test initialization with invalid provider raises error."""
        config = {
            'provider': 'invalid_provider',
        }
        
        with pytest.raises(ConfigurationError):
            EmailClient(config)
    
    def test_init_missing_provider_config(self):
        """Test initialization without required provider config raises error."""
        config = {
            'provider': 'smtp',
            # Missing smtp config
        }
        
        with pytest.raises(ConfigurationError):
            EmailClient(config)


class TestEmailClientFromConfig:
    """Tests for EmailClient.from_config factory method."""
    
    def test_from_yaml_config(self, tmp_path):
        """Test loading configuration from YAML file."""
        config_file = tmp_path / "test-config.yml"
        config_content = """
provider: smtp
smtp:
  host: smtp.example.com
  port: 587
  username: test@example.com
  password: password123
default_from: test@example.com
retry_attempts: 5
timeout: 60
"""
        config_file.write_text(config_content)
        
        client = EmailClient.from_config(str(config_file))
        
        assert client.config.provider.value == 'smtp'
        assert client.config.smtp.host == 'smtp.example.com'
        assert client.config.retry_attempts == 5
        assert client.config.timeout == 60
    
    def test_from_json_config(self, tmp_path):
        """Test loading configuration from JSON file."""
        import json
        
        config_file = tmp_path / "test-config.json"
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
        
        client = EmailClient.from_config(str(config_file))
        
        assert client.config.provider.value == 'gmail'
    
    def test_from_nonexistent_file(self):
        """Test loading from non-existent file raises error."""
        with pytest.raises(ConfigurationError):
            EmailClient.from_config('/nonexistent/path/config.yml')


class TestEmailClientSend:
    """Tests for EmailClient.send method."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        config = {
            'provider': 'smtp',
            'smtp': {
                'host': 'smtp.example.com',
                'port': 587,
                'username': 'test@example.com',
                'password': 'password123',
            },
            'default_from': 'test@example.com',
            'retry_attempts': 1  # Disable retries for faster tests
        }
        return EmailClient(config)
    
    def test_send_validates_recipient(self, client):
        """Test that send validates recipient email."""
        response = client.send(
            to='invalid-email',
            subject='Test',
            text='Hello'
        )
        
        assert response.success is False
        assert 'Invalid' in response.error
    
    def test_send_validates_subject(self, client):
        """Test that send validates subject."""
        response = client.send(
            to='recipient@example.com',
            subject='',  # Empty subject
            text='Hello'
        )
        
        assert response.success is False
        assert 'Subject' in response.error
    
    def test_send_validates_content(self, client):
        """Test that send validates content."""
        response = client.send(
            to='recipient@example.com',
            subject='Test',
            # No text or html content
        )
        
        assert response.success is False
        assert 'content' in response.error.lower()
    
    def test_send_with_cc_bcc(self, client):
        """Test that CC and BCC recipients are validated."""
        response = client.send(
            to='recipient@example.com',
            subject='Test',
            text='Hello',
            cc='invalid-cc-email',
            bcc='recipient@example.com'
        )
        
        assert response.success is False
        assert 'Invalid CC' in response.error
    
    def test_send_without_validation(self, client):
        """Test send with validation disabled (still fails on SMTP connection)."""
        # This will fail at the SMTP level, but validation is skipped
        response = client.send(
            to='invalid-email',
            subject='',
            text='',
            validate=False
        )
        
        # Should fail on SMTP connection, not validation
        assert response.success is False


class TestEmailClientBulk:
    """Tests for EmailClient.send_bulk method."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        config = {
            'provider': 'smtp',
            'smtp': {
                'host': 'smtp.example.com',
                'port': 587,
                'username': 'test@example.com',
                'password': 'password123',
            },
            'default_from': 'test@example.com',
            'retry_attempts': 1
        }
        return EmailClient(config)
    
    def test_send_bulk_returns_bulk_response(self, client):
        """Test that send_bulk returns BulkEmailResponse."""
        messages = [
            EmailMessage(to='user1@example.com', subject='Test 1', text='Hello 1'),
            EmailMessage(to='user2@example.com', subject='Test 2', text='Hello 2'),
        ]
        
        response = client.send_bulk(messages, validate=False)
        
        assert response.total == 2
        assert len(response.responses) == 2


class TestEmailClientContext:
    """Tests for EmailClient context manager."""
    
    def test_context_manager(self):
        """Test using client as context manager."""
        from unittest.mock import patch, MagicMock
        
        config = {
            'provider': 'smtp',
            'smtp': {
                'host': 'smtp.example.com',
                'port': 587,
            },
            'default_from': 'test@example.com'
        }
        
        # Mock SMTP to avoid actual connection
        with patch('smtplib.SMTP') as mock_smtp:
            mock_smtp.return_value = MagicMock()
            with EmailClient(config) as client:
                assert client is not None
                assert client.get_provider_name() == 'smtp'
