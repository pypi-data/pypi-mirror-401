"""
Email response models.

This module defines the EmailResponse class that represents
the result of sending an email.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class EmailStatus(Enum):
    """Email delivery status."""
    PENDING = 'pending'
    SENT = 'sent'
    DELIVERED = 'delivered'
    FAILED = 'failed'
    BOUNCED = 'bounced'
    REJECTED = 'rejected'
    QUEUED = 'queued'


@dataclass
class EmailResponse:
    """
    Represents the response from sending an email.
    
    Attributes:
        success: Whether the email was sent successfully
        message_id: Unique message ID from the provider
        status: Delivery status
        provider: Provider used to send
        timestamp: When the email was sent
        error: Error message if failed
        error_code: Provider-specific error code
        raw_response: Raw response from provider
        recipients: List of recipients
        metadata: Additional metadata
    """
    success: bool
    message_id: Optional[str] = None
    status: EmailStatus = EmailStatus.PENDING
    provider: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    error: Optional[str] = None
    error_code: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None
    recipients: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Set status based on success."""
        if self.success and self.status == EmailStatus.PENDING:
            self.status = EmailStatus.SENT
        elif not self.success and self.status == EmailStatus.PENDING:
            self.status = EmailStatus.FAILED
    
    @property
    def is_successful(self) -> bool:
        """Check if email was sent successfully."""
        return self.success and self.status in (EmailStatus.SENT, EmailStatus.DELIVERED, EmailStatus.QUEUED)
    
    @property
    def is_failed(self) -> bool:
        """Check if email failed to send."""
        return not self.success or self.status in (EmailStatus.FAILED, EmailStatus.BOUNCED, EmailStatus.REJECTED)
    
    @classmethod
    def success_response(cls, message_id: str, provider: str,
                         recipients: List[str] = None,
                         raw_response: Dict[str, Any] = None) -> 'EmailResponse':
        """Create a successful response."""
        return cls(
            success=True,
            message_id=message_id,
            status=EmailStatus.SENT,
            provider=provider,
            recipients=recipients or [],
            raw_response=raw_response
        )
    
    @classmethod
    def failure_response(cls, error: str, provider: str,
                         error_code: str = None,
                         recipients: List[str] = None) -> 'EmailResponse':
        """Create a failure response."""
        return cls(
            success=False,
            status=EmailStatus.FAILED,
            provider=provider,
            error=error,
            error_code=error_code,
            recipients=recipients or []
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            'success': self.success,
            'message_id': self.message_id,
            'status': self.status.value,
            'provider': self.provider,
            'timestamp': self.timestamp.isoformat(),
            'error': self.error,
            'error_code': self.error_code,
            'recipients': self.recipients,
            'metadata': self.metadata
        }
    
    def __str__(self) -> str:
        """String representation."""
        if self.success:
            return f"EmailResponse(success=True, message_id={self.message_id}, provider={self.provider})"
        return f"EmailResponse(success=False, error={self.error})"
    
    def __repr__(self) -> str:
        """Detailed representation."""
        return (f"EmailResponse(success={self.success}, message_id={self.message_id!r}, "
                f"status={self.status.value!r}, provider={self.provider!r}, error={self.error!r})")


@dataclass
class BulkEmailResponse:
    """
    Response from sending bulk emails.
    
    Attributes:
        total: Total number of emails attempted
        successful: Number of successful sends
        failed: Number of failed sends
        responses: Individual responses for each email
    """
    total: int
    successful: int
    failed: int
    responses: List[EmailResponse] = field(default_factory=list)
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total == 0:
            return 0.0
        return self.successful / self.total
    
    @property
    def all_successful(self) -> bool:
        """Check if all emails were sent successfully."""
        return self.failed == 0
    
    @property
    def all_failed(self) -> bool:
        """Check if all emails failed."""
        return self.successful == 0
    
    def get_failed_responses(self) -> List[EmailResponse]:
        """Get only failed responses."""
        return [r for r in self.responses if r.is_failed]
    
    def get_successful_responses(self) -> List[EmailResponse]:
        """Get only successful responses."""
        return [r for r in self.responses if r.is_successful]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'total': self.total,
            'successful': self.successful,
            'failed': self.failed,
            'success_rate': self.success_rate,
            'responses': [r.to_dict() for r in self.responses]
        }
    
    def __str__(self) -> str:
        """String representation."""
        return f"BulkEmailResponse(total={self.total}, successful={self.successful}, failed={self.failed})"
