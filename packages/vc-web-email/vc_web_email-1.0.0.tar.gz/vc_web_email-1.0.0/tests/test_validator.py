"""
Tests for email validator.

This module contains unit tests for the EmailValidator utility class.
"""

import pytest

from vc_web_email import EmailMessage
from vc_web_email.utils.validator import EmailValidator
from vc_web_email.exceptions import ValidationError


class TestEmailValidation:
    """Tests for email address validation."""
    
    def test_valid_emails(self):
        """Test validation of valid email addresses."""
        valid_emails = [
            'user@example.com',
            'user.name@example.com',
            'user+tag@example.com',
            'user@subdomain.example.com',
            'user123@example.co.uk',
            'test_email@domain.org',
            'firstname.lastname@company.com',
        ]
        
        for email in valid_emails:
            assert EmailValidator.validate_email(email) is True, f"Expected {email} to be valid"
    
    def test_invalid_emails(self):
        """Test validation of invalid email addresses."""
        invalid_emails = [
            '',
            'not-an-email',
            '@example.com',
            'user@',
            'user@.com',
            'user@example',
            'user name@example.com',
            'user@@example.com',
        ]
        
        for email in invalid_emails:
            assert EmailValidator.validate_email(email) is False, f"Expected {email} to be invalid"
    
    def test_email_too_long(self):
        """Test that overly long emails are rejected."""
        long_email = 'a' * 250 + '@example.com'
        
        assert EmailValidator.validate_email(long_email) is False
    
    def test_none_email(self):
        """Test that None email is invalid."""
        assert EmailValidator.validate_email(None) is False
    
    def test_validate_email_list(self):
        """Test validating a list of emails."""
        emails = ['valid@example.com', 'invalid-email', 'also-invalid']
        
        invalid = EmailValidator.validate_email_list(emails)
        
        assert len(invalid) == 2
        assert 'invalid-email' in invalid
        assert 'also-invalid' in invalid
    
    def test_validate_single_email_as_list(self):
        """Test validating a single email string."""
        invalid = EmailValidator.validate_email_list('valid@example.com')
        
        assert len(invalid) == 0
    
    def test_strict_validation(self):
        """Test strict RFC 5322 validation."""
        # These might pass permissive but fail strict
        test_emails = [
            ('user@example.com', True),
            ('user.name@example.com', True),
        ]
        
        for email, expected in test_emails:
            result = EmailValidator.validate_email(email, strict=True)
            assert result == expected


class TestMessageValidation:
    """Tests for EmailMessage validation."""
    
    def test_valid_message(self):
        """Test validation of valid message."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test Subject',
            text='Hello, World!'
        )
        
        # Should not raise
        EmailValidator.validate_message(message)
    
    def test_missing_recipient(self):
        """Test validation fails without recipient."""
        message = EmailMessage(
            to=[],
            subject='Test',
            text='Hello'
        )
        
        with pytest.raises(ValidationError) as exc_info:
            EmailValidator.validate_message(message)
        
        assert exc_info.value.field == 'to'
    
    def test_invalid_recipient(self):
        """Test validation fails with invalid recipient."""
        message = EmailMessage(
            to='invalid-email',
            subject='Test',
            text='Hello'
        )
        
        with pytest.raises(ValidationError) as exc_info:
            EmailValidator.validate_message(message)
        
        assert exc_info.value.field == 'to'
        assert 'Invalid' in str(exc_info.value)
    
    def test_invalid_cc(self):
        """Test validation fails with invalid CC."""
        message = EmailMessage(
            to='valid@example.com',
            subject='Test',
            text='Hello',
            cc='invalid-cc'
        )
        
        with pytest.raises(ValidationError) as exc_info:
            EmailValidator.validate_message(message)
        
        assert exc_info.value.field == 'cc'
    
    def test_invalid_bcc(self):
        """Test validation fails with invalid BCC."""
        message = EmailMessage(
            to='valid@example.com',
            subject='Test',
            text='Hello',
            bcc='invalid-bcc'
        )
        
        with pytest.raises(ValidationError) as exc_info:
            EmailValidator.validate_message(message)
        
        assert exc_info.value.field == 'bcc'
    
    def test_invalid_reply_to(self):
        """Test validation fails with invalid reply-to."""
        message = EmailMessage(
            to='valid@example.com',
            subject='Test',
            text='Hello',
            reply_to='invalid-reply-to'
        )
        
        with pytest.raises(ValidationError) as exc_info:
            EmailValidator.validate_message(message)
        
        assert exc_info.value.field == 'reply_to'
    
    def test_invalid_from_email(self):
        """Test validation fails with invalid from email."""
        message = EmailMessage(
            to='valid@example.com',
            subject='Test',
            text='Hello',
            from_email='invalid-from'
        )
        
        with pytest.raises(ValidationError) as exc_info:
            EmailValidator.validate_message(message)
        
        assert exc_info.value.field == 'from_email'
    
    def test_empty_subject(self):
        """Test validation fails with empty subject."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='',
            text='Hello'
        )
        
        with pytest.raises(ValidationError) as exc_info:
            EmailValidator.validate_message(message)
        
        assert exc_info.value.field == 'subject'
    
    def test_whitespace_only_subject(self):
        """Test validation fails with whitespace-only subject."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='   ',
            text='Hello'
        )
        
        with pytest.raises(ValidationError) as exc_info:
            EmailValidator.validate_message(message)
        
        assert exc_info.value.field == 'subject'
    
    def test_subject_too_long(self):
        """Test validation fails with overly long subject."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='X' * 1000,  # Too long
            text='Hello'
        )
        
        with pytest.raises(ValidationError) as exc_info:
            EmailValidator.validate_message(message)
        
        assert exc_info.value.field == 'subject'
        assert 'maximum length' in str(exc_info.value)
    
    def test_missing_content(self):
        """Test validation fails without content."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test'
            # No text, html, or template_id
        )
        
        with pytest.raises(ValidationError) as exc_info:
            EmailValidator.validate_message(message)
        
        assert exc_info.value.field == 'content'
    
    def test_valid_with_html_only(self):
        """Test validation passes with HTML only."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            html='<p>Hello</p>'
        )
        
        # Should not raise
        EmailValidator.validate_message(message)
    
    def test_valid_with_template_id(self):
        """Test validation passes with template_id only."""
        message = EmailMessage(
            to='recipient@example.com',
            subject='Test',
            template_id='template-123'
        )
        
        # Should not raise
        EmailValidator.validate_message(message)
    
    def test_multiple_recipients_validation(self):
        """Test validation with multiple recipients."""
        message = EmailMessage(
            to=['valid@example.com', 'also-valid@example.com'],
            subject='Test',
            text='Hello'
        )
        
        # Should not raise
        EmailValidator.validate_message(message)
    
    def test_one_invalid_recipient_fails(self):
        """Test validation fails if one recipient is invalid."""
        message = EmailMessage(
            to=['valid@example.com', 'invalid-email'],
            subject='Test',
            text='Hello'
        )
        
        with pytest.raises(ValidationError):
            EmailValidator.validate_message(message)


class TestSanitization:
    """Tests for email sanitization."""
    
    def test_sanitize_email(self):
        """Test email sanitization."""
        assert EmailValidator.sanitize_email('  User@Example.com  ') == 'user@example.com'
        assert EmailValidator.sanitize_email('USER@DOMAIN.COM') == 'user@domain.com'
    
    def test_sanitize_none(self):
        """Test sanitizing None returns None."""
        assert EmailValidator.sanitize_email(None) is None
    
    def test_sanitize_empty(self):
        """Test sanitizing empty string returns empty."""
        assert EmailValidator.sanitize_email('') == ''


class TestEmailExtraction:
    """Tests for email extraction."""
    
    def test_extract_from_angle_brackets(self):
        """Test extracting email from angle bracket format."""
        result = EmailValidator.extract_email('John Doe <john@example.com>')
        
        assert result == 'john@example.com'
    
    def test_extract_plain_email(self):
        """Test extracting plain email."""
        result = EmailValidator.extract_email('john@example.com')
        
        assert result == 'john@example.com'
    
    def test_extract_from_none(self):
        """Test extracting from None returns None."""
        result = EmailValidator.extract_email(None)
        
        assert result is None
    
    def test_extract_from_empty(self):
        """Test extracting from empty string returns None."""
        result = EmailValidator.extract_email('')
        
        assert result is None


class TestEmailFormatting:
    """Tests for email formatting."""
    
    def test_format_with_name(self):
        """Test formatting email with display name."""
        result = EmailValidator.format_email('john@example.com', 'John Doe')
        
        assert result == 'John Doe <john@example.com>'
    
    def test_format_without_name(self):
        """Test formatting email without display name."""
        result = EmailValidator.format_email('john@example.com')
        
        assert result == 'john@example.com'
    
    def test_format_sanitizes(self):
        """Test that formatting also sanitizes the email."""
        result = EmailValidator.format_email('  JOHN@EXAMPLE.COM  ', 'John Doe')
        
        assert result == 'John Doe <john@example.com>'
