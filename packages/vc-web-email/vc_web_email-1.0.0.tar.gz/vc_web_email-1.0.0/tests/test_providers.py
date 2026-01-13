"""
Tests for email providers.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from vc_web_email.config import EmailConfig, SMTPConfig, GmailConfig, SendGridConfig
from vc_web_email.config import EmailProvider, AWSSESConfig, MailgunConfig, OutlookConfig
from vc_web_email.message import EmailMessage
from vc_web_email.providers.smtp import SMTPProvider
from vc_web_email.providers.gmail import GmailProvider
from vc_web_email.providers.sendgrid import SendGridProvider
from vc_web_email.providers.outlook import OutlookProvider


class TestSMTPProvider:
    """Tests for SMTP provider."""
    
    @pytest.fixture
    def smtp_config(self):
        return EmailConfig(
            provider=EmailProvider.SMTP,
            smtp=SMTPConfig(
                host='smtp.example.com',
                port=587,
                username='user@example.com',
                password='password'
            ),
            default_from='user@example.com'
        )
    
    def test_provider_name(self, smtp_config):
        provider = SMTPProvider(smtp_config)
        assert provider.name == 'smtp'
    
    def test_get_from_address(self, smtp_config):
        provider = SMTPProvider(smtp_config)
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            text='Hello'
        )
        from_addr = provider._get_from_address(message)
        assert from_addr == 'user@example.com'
    
    def test_get_from_address_with_override(self, smtp_config):
        provider = SMTPProvider(smtp_config)
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            text='Hello',
            from_email='override@example.com'
        )
        from_addr = provider._get_from_address(message)
        assert from_addr == 'override@example.com'
    
    @patch('smtplib.SMTP')
    def test_connect(self, mock_smtp_class, smtp_config):
        mock_smtp = MagicMock()
        mock_smtp_class.return_value = mock_smtp
        
        provider = SMTPProvider(smtp_config)
        provider.connect()
        
        mock_smtp_class.assert_called_once()
        mock_smtp.starttls.assert_called_once()
        mock_smtp.login.assert_called_once()
    
    @patch('smtplib.SMTP')
    def test_disconnect(self, mock_smtp_class, smtp_config):
        mock_smtp = MagicMock()
        mock_smtp_class.return_value = mock_smtp
        
        provider = SMTPProvider(smtp_config)
        provider.connect()
        provider.disconnect()
        
        mock_smtp.quit.assert_called_once()


class TestGmailProvider:
    """Tests for Gmail provider."""
    
    @pytest.fixture
    def gmail_config(self):
        return EmailConfig(
            provider=EmailProvider.GMAIL,
            gmail=GmailConfig(
                username='user@gmail.com',
                password='app-password'
            ),
            default_from='user@gmail.com'
        )
    
    def test_provider_name(self, gmail_config):
        provider = GmailProvider(gmail_config)
        assert provider.name == 'gmail'
    
    def test_uses_gmail_smtp_server(self, gmail_config):
        provider = GmailProvider(gmail_config)
        assert provider._smtp_config.host == 'smtp.gmail.com'
        assert provider._smtp_config.port == 587


class TestOutlookProvider:
    """Tests for Outlook provider."""
    
    @pytest.fixture
    def outlook_config(self):
        return EmailConfig(
            provider=EmailProvider.OUTLOOK,
            outlook=OutlookConfig(
                username='user@outlook.com',
                password='password'
            ),
            default_from='user@outlook.com'
        )
    
    def test_provider_name(self, outlook_config):
        provider = OutlookProvider(outlook_config)
        assert provider.name == 'outlook'
    
    def test_uses_outlook_smtp_server(self, outlook_config):
        provider = OutlookProvider(outlook_config)
        assert provider._smtp_config.host == 'smtp-mail.outlook.com'
        assert provider._smtp_config.port == 587


class TestSendGridProvider:
    """Tests for SendGrid provider."""
    
    @pytest.fixture
    def sendgrid_config(self):
        return EmailConfig(
            provider=EmailProvider.SENDGRID,
            sendgrid=SendGridConfig(api_key='SG.test-key'),
            default_from='sender@example.com'
        )
    
    def test_provider_name(self, sendgrid_config):
        provider = SendGridProvider(sendgrid_config)
        assert provider.name == 'sendgrid'
    
    def test_build_api_payload(self, sendgrid_config):
        provider = SendGridProvider(sendgrid_config)
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test Subject',
            text='Hello',
            html='<p>Hello</p>'
        )
        
        payload = provider._build_api_payload(message)
        
        assert payload['from']['email'] == 'sender@example.com'
        assert payload['subject'] == 'Test Subject'
        assert len(payload['personalizations'][0]['to']) == 1
        assert len(payload['content']) == 2
