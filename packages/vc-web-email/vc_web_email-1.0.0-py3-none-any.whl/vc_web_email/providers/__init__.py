"""
Email providers package.
"""

from .base import BaseEmailProvider
from .smtp import SMTPProvider
from .gmail import GmailProvider
from .sendgrid import SendGridProvider
from .aws_ses import AWSSESProvider
from .mailgun import MailgunProvider
from .outlook import OutlookProvider

__all__ = [
    'BaseEmailProvider',
    'SMTPProvider',
    'GmailProvider',
    'SendGridProvider',
    'AWSSESProvider',
    'MailgunProvider',
    'OutlookProvider'
]
