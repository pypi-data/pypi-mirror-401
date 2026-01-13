"""
Email message and attachment models.

This module defines the EmailMessage and Attachment dataclasses
used to construct email messages.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Any
from pathlib import Path
import base64
import mimetypes
import os

from .exceptions import AttachmentError


@dataclass
class Attachment:
    """
    Represents an email attachment.
    
    Attributes:
        filename: Name of the file
        content: File content as bytes or base64 string
        content_type: MIME type of the file
        content_id: Content ID for inline attachments
        is_inline: Whether the attachment is inline
    """
    filename: str
    content: Union[bytes, str]
    content_type: Optional[str] = None
    content_id: Optional[str] = None
    is_inline: bool = False
    
    def __post_init__(self):
        """Validate and process attachment data."""
        if not self.filename:
            raise AttachmentError("Attachment filename cannot be empty")
        
        # Auto-detect content type if not provided
        if not self.content_type:
            self.content_type = mimetypes.guess_type(self.filename)[0] or 'application/octet-stream'
        
        # Convert string content to bytes if it's base64
        if isinstance(self.content, str):
            try:
                self.content = base64.b64decode(self.content)
            except Exception:
                # If not valid base64, treat as text
                self.content = self.content.encode('utf-8')
    
    @classmethod
    def from_file(cls, filepath: Union[str, Path], 
                  content_type: Optional[str] = None,
                  filename: Optional[str] = None) -> 'Attachment':
        """
        Create an attachment from a file path.
        
        Args:
            filepath: Path to the file
            content_type: Optional MIME type override
            filename: Optional filename override
        
        Returns:
            Attachment instance
        
        Raises:
            AttachmentError: If file cannot be read
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise AttachmentError(f"File not found: {filepath}", filename=str(filepath))
        
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
        except IOError as e:
            raise AttachmentError(f"Error reading file: {e}", filename=str(filepath))
        
        return cls(
            filename=filename or filepath.name,
            content=content,
            content_type=content_type
        )
    
    @classmethod
    def from_base64(cls, filename: str, base64_content: str,
                    content_type: Optional[str] = None) -> 'Attachment':
        """
        Create an attachment from base64 encoded content.
        
        Args:
            filename: Name for the attachment
            base64_content: Base64 encoded file content
            content_type: Optional MIME type
        
        Returns:
            Attachment instance
        """
        try:
            content = base64.b64decode(base64_content)
        except Exception as e:
            raise AttachmentError(f"Invalid base64 content: {e}", filename=filename)
        
        return cls(
            filename=filename,
            content=content,
            content_type=content_type
        )
    
    def get_base64(self) -> str:
        """Return content as base64 encoded string."""
        if isinstance(self.content, bytes):
            return base64.b64encode(self.content).decode('utf-8')
        return self.content
    
    @property
    def size(self) -> int:
        """Return size of attachment in bytes."""
        if isinstance(self.content, bytes):
            return len(self.content)
        return len(self.content.encode('utf-8'))


@dataclass
class EmailMessage:
    """
    Represents an email message.
    
    Attributes:
        to: Recipient email address(es)
        subject: Email subject
        text: Plain text body
        html: HTML body
        from_email: Sender email address (overrides default)
        cc: CC recipients
        bcc: BCC recipients
        reply_to: Reply-to address
        attachments: List of attachments
        headers: Custom email headers
        tags: Tags for tracking/categorization
        metadata: Additional metadata
        template_id: Template ID for provider templates
        template_data: Data for template substitution
    """
    to: Union[str, List[str]]
    subject: str
    text: Optional[str] = None
    html: Optional[str] = None
    from_email: Optional[str] = None
    cc: Optional[Union[str, List[str]]] = None
    bcc: Optional[Union[str, List[str]]] = None
    reply_to: Optional[str] = None
    attachments: List[Attachment] = field(default_factory=list)
    headers: Dict[str, str] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    template_id: Optional[str] = None
    template_data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Normalize recipient fields."""
        # Convert single recipient to list
        if isinstance(self.to, str):
            self.to = [self.to]
        if isinstance(self.cc, str):
            self.cc = [self.cc]
        if isinstance(self.bcc, str):
            self.bcc = [self.bcc]
    
    def add_attachment(self, attachment: Union[Attachment, str, Path]) -> 'EmailMessage':
        """
        Add an attachment to the message.
        
        Args:
            attachment: Attachment object or file path
        
        Returns:
            Self for chaining
        """
        if isinstance(attachment, (str, Path)):
            attachment = Attachment.from_file(attachment)
        self.attachments.append(attachment)
        return self
    
    def add_attachment_from_base64(self, filename: str, base64_content: str,
                                    content_type: Optional[str] = None) -> 'EmailMessage':
        """
        Add an attachment from base64 content.
        
        Args:
            filename: Name for the attachment
            base64_content: Base64 encoded content
            content_type: Optional MIME type
        
        Returns:
            Self for chaining
        """
        attachment = Attachment.from_base64(filename, base64_content, content_type)
        self.attachments.append(attachment)
        return self
    
    def get_all_recipients(self) -> List[str]:
        """Get all recipients (to, cc, bcc combined)."""
        recipients = list(self.to) if self.to else []
        if self.cc:
            recipients.extend(self.cc)
        if self.bcc:
            recipients.extend(self.bcc)
        return recipients
    
    def has_content(self) -> bool:
        """Check if message has either text or HTML content."""
        return bool(self.text or self.html or self.template_id)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            'to': self.to,
            'subject': self.subject,
            'text': self.text,
            'html': self.html,
            'from_email': self.from_email,
            'cc': self.cc,
            'bcc': self.bcc,
            'reply_to': self.reply_to,
            'attachments': [
                {
                    'filename': a.filename,
                    'content_type': a.content_type,
                    'size': a.size
                }
                for a in self.attachments
            ],
            'headers': self.headers,
            'tags': self.tags,
            'metadata': self.metadata,
            'template_id': self.template_id,
            'template_data': self.template_data
        }
