"""
Email validation utilities.

This module provides validation functions for email addresses,
messages, and other email-related data.
"""

import re
from typing import List, Optional, Union
from ..message import EmailMessage
from ..exceptions import ValidationError


class EmailValidator:
    """
    Email validation utilities.
    
    Provides methods for validating email addresses, messages,
    and other email-related data.
    """
    
    # RFC 5322 compliant email regex (simplified but comprehensive)
    EMAIL_REGEX = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    # More permissive email regex
    EMAIL_REGEX_PERMISSIVE = re.compile(
        r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    )
    
    # Maximum lengths
    MAX_EMAIL_LENGTH = 254
    MAX_SUBJECT_LENGTH = 988  # Most servers limit to ~1000 chars
    MAX_ATTACHMENT_SIZE = 25 * 1024 * 1024  # 25 MB
    MAX_TOTAL_ATTACHMENTS_SIZE = 25 * 1024 * 1024  # 25 MB total
    
    @classmethod
    def validate_email(cls, email: str, strict: bool = False) -> bool:
        """
        Validate an email address format.
        
        Args:
            email: Email address to validate
            strict: Use strict RFC 5322 validation
        
        Returns:
            True if valid, False otherwise
        """
        if not email or not isinstance(email, str):
            return False
        
        email = email.strip()
        
        if len(email) > cls.MAX_EMAIL_LENGTH:
            return False
        
        pattern = cls.EMAIL_REGEX if strict else cls.EMAIL_REGEX_PERMISSIVE
        return bool(pattern.match(email))
    
    @classmethod
    def validate_email_list(cls, emails: Union[str, List[str]], strict: bool = False) -> List[str]:
        """
        Validate a list of email addresses.
        
        Args:
            emails: Single email or list of emails
            strict: Use strict validation
        
        Returns:
            List of invalid email addresses
        
        Raises:
            ValidationError: If any email is invalid
        """
        if isinstance(emails, str):
            emails = [emails]
        
        invalid_emails = []
        for email in emails:
            if not cls.validate_email(email, strict):
                invalid_emails.append(email)
        
        return invalid_emails
    
    @classmethod
    def validate_message(cls, message: EmailMessage) -> None:
        """
        Validate an email message.
        
        Args:
            message: EmailMessage to validate
        
        Raises:
            ValidationError: If validation fails
        """
        # Validate recipients
        if not message.to or len(message.to) == 0:
            raise ValidationError("At least one recipient is required", field="to")
        
        invalid_to = cls.validate_email_list(message.to)
        if invalid_to:
            raise ValidationError(
                f"Invalid recipient email address(es): {', '.join(invalid_to)}",
                field="to"
            )
        
        # Validate CC
        if message.cc:
            invalid_cc = cls.validate_email_list(message.cc)
            if invalid_cc:
                raise ValidationError(
                    f"Invalid CC email address(es): {', '.join(invalid_cc)}",
                    field="cc"
                )
        
        # Validate BCC
        if message.bcc:
            invalid_bcc = cls.validate_email_list(message.bcc)
            if invalid_bcc:
                raise ValidationError(
                    f"Invalid BCC email address(es): {', '.join(invalid_bcc)}",
                    field="bcc"
                )
        
        # Validate reply-to
        if message.reply_to and not cls.validate_email(message.reply_to):
            raise ValidationError(
                f"Invalid reply-to email address: {message.reply_to}",
                field="reply_to"
            )
        
        # Validate from email
        if message.from_email and not cls.validate_email(message.from_email):
            raise ValidationError(
                f"Invalid from email address: {message.from_email}",
                field="from_email"
            )
        
        # Validate subject
        if not message.subject or not message.subject.strip():
            raise ValidationError("Subject is required", field="subject")
        
        if len(message.subject) > cls.MAX_SUBJECT_LENGTH:
            raise ValidationError(
                f"Subject exceeds maximum length of {cls.MAX_SUBJECT_LENGTH} characters",
                field="subject"
            )
        
        # Validate content
        if not message.has_content():
            raise ValidationError(
                "Email must have either text, HTML content, or template_id",
                field="content"
            )
        
        # Validate attachments
        cls.validate_attachments(message)
    
    @classmethod
    def validate_attachments(cls, message: EmailMessage) -> None:
        """
        Validate email attachments.
        
        Args:
            message: EmailMessage with attachments to validate
        
        Raises:
            ValidationError: If attachment validation fails
        """
        if not message.attachments:
            return
        
        total_size = 0
        
        for attachment in message.attachments:
            # Check individual attachment size
            if attachment.size > cls.MAX_ATTACHMENT_SIZE:
                raise ValidationError(
                    f"Attachment '{attachment.filename}' exceeds maximum size of "
                    f"{cls.MAX_ATTACHMENT_SIZE / (1024 * 1024):.0f} MB",
                    field="attachments",
                    details={'filename': attachment.filename, 'size': attachment.size}
                )
            
            total_size += attachment.size
        
        # Check total attachments size
        if total_size > cls.MAX_TOTAL_ATTACHMENTS_SIZE:
            raise ValidationError(
                f"Total attachments size exceeds maximum of "
                f"{cls.MAX_TOTAL_ATTACHMENTS_SIZE / (1024 * 1024):.0f} MB",
                field="attachments",
                details={'total_size': total_size}
            )
    
    @classmethod
    def sanitize_email(cls, email: str) -> str:
        """
        Sanitize an email address by stripping whitespace and lowercasing.
        
        Args:
            email: Email address to sanitize
        
        Returns:
            Sanitized email address
        """
        if not email:
            return email
        return email.strip().lower()
    
    @classmethod
    def extract_email(cls, text: str) -> Optional[str]:
        """
        Extract an email address from text that may contain name + email.
        
        Examples:
            "John Doe <john@example.com>" -> "john@example.com"
            "john@example.com" -> "john@example.com"
        
        Args:
            text: Text containing an email address
        
        Returns:
            Extracted email address or None
        """
        if not text:
            return None
        
        # Try to extract from format: Name <email@domain.com>
        match = re.search(r'<([^>]+)>', text)
        if match:
            return cls.sanitize_email(match.group(1))
        
        # Try to find email in plain text
        match = cls.EMAIL_REGEX_PERMISSIVE.search(text)
        if match:
            return cls.sanitize_email(match.group(0))
        
        return None
    
    @classmethod
    def format_email(cls, email: str, name: Optional[str] = None) -> str:
        """
        Format an email address with optional display name.
        
        Args:
            email: Email address
            name: Optional display name
        
        Returns:
            Formatted email string
        """
        email = cls.sanitize_email(email)
        if name:
            return f"{name} <{email}>"
        return email
