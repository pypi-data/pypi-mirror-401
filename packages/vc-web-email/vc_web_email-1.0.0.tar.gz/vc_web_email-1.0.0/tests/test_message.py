"""
Tests for EmailMessage and Attachment.

This module contains unit tests for the EmailMessage and Attachment classes.
"""

import pytest
import base64
import tempfile
from pathlib import Path

from vc_web_email import EmailMessage, Attachment
from vc_web_email.exceptions import AttachmentError


class TestAttachment:
    """Tests for Attachment class."""
    
    def test_create_attachment_with_bytes(self):
        """Test creating attachment with bytes content."""
        content = b'Hello, World!'
        attachment = Attachment(
            filename='test.txt',
            content=content,
            content_type='text/plain'
        )
        
        assert attachment.filename == 'test.txt'
        assert attachment.content == content
        assert attachment.content_type == 'text/plain'
        assert attachment.size == len(content)
    
    def test_create_attachment_with_base64_string(self):
        """Test creating attachment with base64 string."""
        original = b'Hello, World!'
        base64_content = base64.b64encode(original).decode('utf-8')
        
        attachment = Attachment(
            filename='test.txt',
            content=base64_content,
            content_type='text/plain'
        )
        
        assert attachment.content == original
    
    def test_auto_detect_content_type(self):
        """Test automatic content type detection."""
        attachment = Attachment(
            filename='document.pdf',
            content=b'PDF content'
        )
        
        assert attachment.content_type == 'application/pdf'
    
    def test_attachment_from_file(self, tmp_path):
        """Test creating attachment from file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")
        
        attachment = Attachment.from_file(test_file)
        
        assert attachment.filename == 'test.txt'
        assert attachment.content == b'Hello, World!'
        assert attachment.content_type == 'text/plain'
    
    def test_attachment_from_nonexistent_file(self):
        """Test creating attachment from non-existent file raises error."""
        with pytest.raises(AttachmentError):
            Attachment.from_file('/nonexistent/file.txt')
    
    def test_attachment_from_base64(self):
        """Test creating attachment from base64."""
        original = b'Binary data'
        base64_content = base64.b64encode(original).decode('utf-8')
        
        attachment = Attachment.from_base64(
            filename='data.bin',
            base64_content=base64_content
        )
        
        assert attachment.content == original
    
    def test_get_base64(self):
        """Test getting content as base64."""
        content = b'Hello, World!'
        attachment = Attachment(filename='test.txt', content=content)
        
        base64_result = attachment.get_base64()
        
        assert base64.b64decode(base64_result) == content
    
    def test_empty_filename_raises_error(self):
        """Test that empty filename raises error."""
        with pytest.raises(AttachmentError):
            Attachment(filename='', content=b'data')
    
    def test_inline_attachment(self):
        """Test inline attachment properties."""
        attachment = Attachment(
            filename='image.png',
            content=b'PNG data',
            content_id='img001',
            is_inline=True
        )
        
        assert attachment.is_inline is True
        assert attachment.content_id == 'img001'


class TestEmailMessage:
    """Tests for EmailMessage class."""
    
    def test_create_simple_message(self):
        """Test creating a simple email message."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test Subject',
            text='Hello, World!'
        )
        
        assert message.to == ['recipient@example.com']
        assert message.subject == 'Test Subject'
        assert message.text == 'Hello, World!'
    
    def test_create_message_with_html(self):
        """Test creating message with HTML content."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='HTML Test',
            html='<h1>Hello</h1>'
        )
        
        assert message.html == '<h1>Hello</h1>'
        assert message.has_content() is True
    
    def test_multiple_recipients(self):
        """Test message with multiple recipients."""
        message = EmailMessage(
            to=['user1@example.com', 'user2@example.com'],
            subject='Test',
            text='Hello'
        )
        
        assert len(message.to) == 2
        assert 'user1@example.com' in message.to
        assert 'user2@example.com' in message.to
    
    def test_single_recipient_converts_to_list(self):
        """Test that single recipient string is converted to list."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            text='Hello'
        )
        
        assert isinstance(message.to, list)
        assert len(message.to) == 1
    
    def test_cc_and_bcc(self):
        """Test CC and BCC recipients."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            text='Hello',
            cc='cc@example.com',
            bcc=['bcc1@example.com', 'bcc2@example.com']
        )
        
        assert message.cc == ['cc@example.com']
        assert len(message.bcc) == 2
    
    def test_get_all_recipients(self):
        """Test getting all recipients."""
        message = EmailMessage(
            to='to@example.com',
            subject='Test',
            text='Hello',
            cc='cc@example.com',
            bcc='bcc@example.com'
        )
        
        all_recipients = message.get_all_recipients()
        
        assert len(all_recipients) == 3
        assert 'to@example.com' in all_recipients
        assert 'cc@example.com' in all_recipients
        assert 'bcc@example.com' in all_recipients
    
    def test_add_attachment(self):
        """Test adding attachment to message."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            text='Hello'
        )
        
        attachment = Attachment(filename='test.txt', content=b'data')
        message.add_attachment(attachment)
        
        assert len(message.attachments) == 1
        assert message.attachments[0].filename == 'test.txt'
    
    def test_add_attachment_from_path(self, tmp_path):
        """Test adding attachment from file path."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello")
        
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            text='Hello'
        )
        
        result = message.add_attachment(test_file)
        
        assert result is message  # Chaining
        assert len(message.attachments) == 1
    
    def test_add_attachment_from_base64(self):
        """Test adding attachment from base64."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            text='Hello'
        )
        
        base64_content = base64.b64encode(b'data').decode('utf-8')
        result = message.add_attachment_from_base64(
            filename='test.bin',
            base64_content=base64_content
        )
        
        assert result is message  # Chaining
        assert len(message.attachments) == 1
    
    def test_has_content_with_text(self):
        """Test has_content with text."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            text='Hello'
        )
        
        assert message.has_content() is True
    
    def test_has_content_with_html(self):
        """Test has_content with HTML."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            html='<p>Hello</p>'
        )
        
        assert message.has_content() is True
    
    def test_has_content_with_template(self):
        """Test has_content with template."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            template_id='template-123'
        )
        
        assert message.has_content() is True
    
    def test_has_content_without_content(self):
        """Test has_content without any content."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test'
        )
        
        assert message.has_content() is False
    
    def test_to_dict(self):
        """Test converting message to dictionary."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            text='Hello',
            html='<p>Hello</p>',
            from_email='sender@example.com',
            tags=['important', 'test'],
            metadata={'campaign': 'test-campaign'}
        )
        
        result = message.to_dict()
        
        assert result['to'] == ['recipient@example.com']
        assert result['subject'] == 'Test'
        assert result['text'] == 'Hello'
        assert result['html'] == '<p>Hello</p>'
        assert result['from_email'] == 'sender@example.com'
        assert 'important' in result['tags']
    
    def test_custom_headers(self):
        """Test custom email headers."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            text='Hello',
            headers={
                'X-Custom-Header': 'custom-value',
                'X-Priority': '1'
            }
        )
        
        assert message.headers['X-Custom-Header'] == 'custom-value'
        assert message.headers['X-Priority'] == '1'
    
    def test_reply_to(self):
        """Test reply-to address."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            text='Hello',
            reply_to='reply@example.com'
        )
        
        assert message.reply_to == 'reply@example.com'
    
    def test_from_email_override(self):
        """Test from email override."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            text='Hello',
            from_email='custom-sender@example.com'
        )
        
        assert message.from_email == 'custom-sender@example.com'
