"""
AWS SES email provider.

This module implements the AWS SES email provider for sending emails
through Amazon Simple Email Service.
"""

from typing import Optional, Dict, Any
import base64

from .base import BaseEmailProvider
from ..config import EmailConfig
from ..message import EmailMessage
from ..response import EmailResponse
from ..exceptions import ProviderError, AuthenticationError


class AWSSESProvider(BaseEmailProvider):
    """
    AWS SES email provider.
    
    Sends emails through AWS Simple Email Service.
    """
    
    def __init__(self, config: EmailConfig):
        """
        Initialize AWS SES provider.
        
        Args:
            config: Email configuration with AWS SES settings
        """
        super().__init__(config)
        self._ses_config = config.aws_ses
        self._client = None
    
    @property
    def name(self) -> str:
        return 'aws_ses'
    
    def connect(self) -> None:
        """Initialize boto3 SES client."""
        try:
            import boto3
            
            # Build client kwargs
            client_kwargs = {
                'region_name': self._ses_config.region
            }
            
            if self._ses_config.access_key_id and self._ses_config.secret_access_key:
                client_kwargs['aws_access_key_id'] = self._ses_config.access_key_id
                client_kwargs['aws_secret_access_key'] = self._ses_config.secret_access_key
            
            self._client = boto3.client('ses', **client_kwargs)
        
        except ImportError:
            raise ProviderError(
                "boto3 is required for AWS SES. Install with: pip install boto3",
                provider=self.name
            )
        except Exception as e:
            raise AuthenticationError(
                f"Failed to initialize AWS SES client: {e}",
                provider=self.name
            )
    
    def disconnect(self) -> None:
        """Close SES client."""
        self._client = None
    
    def send(self, message: EmailMessage) -> EmailResponse:
        """
        Send an email via AWS SES.
        
        Args:
            message: Email message to send
        
        Returns:
            EmailResponse with send result
        """
        try:
            if not self._client:
                self.connect()
            
            # Determine whether to use raw email or structured API
            if message.attachments:
                return self._send_raw_email(message)
            else:
                return self._send_email(message)
        
        except Exception as e:
            return EmailResponse.failure_response(
                error=f"AWS SES error: {e}",
                provider=self.name,
                recipients=message.get_all_recipients()
            )
    
    def _send_email(self, message: EmailMessage) -> EmailResponse:
        """Send email using SES send_email API."""
        destination = {
            'ToAddresses': message.to
        }
        
        if message.cc:
            destination['CcAddresses'] = message.cc
        
        if message.bcc:
            destination['BccAddresses'] = message.bcc
        
        # Build message body
        body = {}
        if message.text:
            body['Text'] = {
                'Data': message.text,
                'Charset': 'UTF-8'
            }
        
        if message.html:
            body['Html'] = {
                'Data': message.html,
                'Charset': 'UTF-8'
            }
        
        email_message = {
            'Subject': {
                'Data': message.subject,
                'Charset': 'UTF-8'
            },
            'Body': body
        }
        
        # Build send kwargs
        send_kwargs = {
            'Source': self._get_from_address(message),
            'Destination': destination,
            'Message': email_message
        }
        
        reply_to = self._get_reply_to(message)
        if reply_to:
            send_kwargs['ReplyToAddresses'] = [reply_to]
        
        if self._ses_config.configuration_set:
            send_kwargs['ConfigurationSetName'] = self._ses_config.configuration_set
        
        # Send email
        response = self._client.send_email(**send_kwargs)
        
        return EmailResponse.success_response(
            message_id=response.get('MessageId', ''),
            provider=self.name,
            recipients=message.get_all_recipients(),
            raw_response=response
        )
    
    def _send_raw_email(self, message: EmailMessage) -> EmailResponse:
        """Send email with attachments using raw email API."""
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        from email.utils import formatdate
        
        # Create MIME message
        mime_msg = MIMEMultipart('mixed')
        
        # Set headers
        mime_msg['From'] = self._get_from_address(message)
        mime_msg['To'] = ', '.join(message.to)
        mime_msg['Subject'] = message.subject
        mime_msg['Date'] = formatdate(localtime=True)
        
        if message.cc:
            mime_msg['Cc'] = ', '.join(message.cc)
        
        reply_to = self._get_reply_to(message)
        if reply_to:
            mime_msg['Reply-To'] = reply_to
        
        # Add body
        msg_alternative = MIMEMultipart('alternative')
        mime_msg.attach(msg_alternative)
        
        if message.text:
            text_part = MIMEText(message.text, 'plain', 'utf-8')
            msg_alternative.attach(text_part)
        
        if message.html:
            html_part = MIMEText(message.html, 'html', 'utf-8')
            msg_alternative.attach(html_part)
        
        # Add attachments
        for attachment in message.attachments:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.content)
            encoders.encode_base64(part)
            
            if attachment.is_inline and attachment.content_id:
                part.add_header('Content-ID', f'<{attachment.content_id}>')
                part.add_header('Content-Disposition', 'inline', filename=attachment.filename)
            else:
                part.add_header('Content-Disposition', 'attachment', filename=attachment.filename)
            
            if attachment.content_type:
                part.replace_header('Content-Type', attachment.content_type)
            
            mime_msg.attach(part)
        
        # Build destinations
        destinations = list(message.to)
        if message.cc:
            destinations.extend(message.cc)
        if message.bcc:
            destinations.extend(message.bcc)
        
        # Send raw email
        send_kwargs = {
            'Source': self._get_from_address(message),
            'Destinations': destinations,
            'RawMessage': {
                'Data': mime_msg.as_string()
            }
        }
        
        if self._ses_config.configuration_set:
            send_kwargs['ConfigurationSetName'] = self._ses_config.configuration_set
        
        response = self._client.send_raw_email(**send_kwargs)
        
        return EmailResponse.success_response(
            message_id=response.get('MessageId', ''),
            provider=self.name,
            recipients=message.get_all_recipients(),
            raw_response=response
        )
