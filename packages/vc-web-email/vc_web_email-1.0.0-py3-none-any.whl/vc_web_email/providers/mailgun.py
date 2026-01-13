"""
Mailgun email provider.

This module implements the Mailgun email provider for sending emails
through the Mailgun API.
"""

import json
from typing import Optional, Dict, Any
import base64
import urllib.request
import urllib.error
import urllib.parse

from .base import BaseEmailProvider
from ..config import EmailConfig
from ..message import EmailMessage
from ..response import EmailResponse
from ..exceptions import ProviderError, AuthenticationError


class MailgunProvider(BaseEmailProvider):
    """
    Mailgun email provider.
    
    Sends emails through Mailgun's API.
    """
    
    def __init__(self, config: EmailConfig):
        """
        Initialize Mailgun provider.
        
        Args:
            config: Email configuration with Mailgun settings
        """
        super().__init__(config)
        self._api_key = config.mailgun.api_key
        self._domain = config.mailgun.domain
        self._base_url = config.mailgun.base_url
    
    @property
    def name(self) -> str:
        return 'mailgun'
    
    def send(self, message: EmailMessage) -> EmailResponse:
        """
        Send an email via Mailgun API.
        
        Args:
            message: Email message to send
        
        Returns:
            EmailResponse with send result
        """
        try:
            url = f"{self._base_url}/{self._domain}/messages"
            
            # Build form data
            data = {
                'from': self._get_from_address(message),
                'subject': message.subject
            }
            
            # Add recipients
            data['to'] = ', '.join(message.to)
            
            if message.cc:
                data['cc'] = ', '.join(message.cc)
            
            if message.bcc:
                data['bcc'] = ', '.join(message.bcc)
            
            # Add content
            if message.text:
                data['text'] = message.text
            
            if message.html:
                data['html'] = message.html
            
            # Add reply-to
            reply_to = self._get_reply_to(message)
            if reply_to:
                data['h:Reply-To'] = reply_to
            
            # Add custom headers
            for key, value in message.headers.items():
                data[f'h:{key}'] = value
            
            # Add tags
            if message.tags:
                data['o:tag'] = message.tags
            
            # Encode data
            encoded_data = urllib.parse.urlencode(data, doseq=True).encode('utf-8')
            
            # Create request with basic auth
            credentials = base64.b64encode(f'api:{self._api_key}'.encode()).decode()
            headers = {
                'Authorization': f'Basic {credentials}'
            }
            
            req = urllib.request.Request(url, data=encoded_data, headers=headers, method='POST')
            
            # Handle attachments separately if present
            if message.attachments:
                return self._send_with_attachments(message)
            
            # Send request
            with urllib.request.urlopen(req, timeout=self.config.timeout) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                
                return EmailResponse.success_response(
                    message_id=response_data.get('id', ''),
                    provider=self.name,
                    recipients=message.get_all_recipients(),
                    raw_response=response_data
                )
        
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ''
            try:
                error_data = json.loads(error_body)
                error_message = error_data.get('message', error_body)
            except json.JSONDecodeError:
                error_message = error_body
            
            return EmailResponse.failure_response(
                error=f"Mailgun API error: {e.code} - {error_message}",
                provider=self.name,
                error_code=str(e.code),
                recipients=message.get_all_recipients()
            )
        except Exception as e:
            return EmailResponse.failure_response(
                error=f"Mailgun error: {e}",
                provider=self.name,
                recipients=message.get_all_recipients()
            )
    
    def _send_with_attachments(self, message: EmailMessage) -> EmailResponse:
        """
        Send email with attachments using multipart form data.
        
        Args:
            message: Email message with attachments
        
        Returns:
            EmailResponse with send result
        """
        try:
            import mimetypes
            from email.mime.multipart import MIMEMultipart
            from email.mime.base import MIMEBase
            from email.mime.text import MIMEText
            from email.mime.application import MIMEApplication
            import io
            
            url = f"{self._base_url}/{self._domain}/messages"
            
            # Create multipart form data manually
            boundary = '----VCWebEmailBoundary'
            
            parts = []
            
            # Add form fields
            fields = {
                'from': self._get_from_address(message),
                'to': ', '.join(message.to),
                'subject': message.subject
            }
            
            if message.cc:
                fields['cc'] = ', '.join(message.cc)
            
            if message.bcc:
                fields['bcc'] = ', '.join(message.bcc)
            
            if message.text:
                fields['text'] = message.text
            
            if message.html:
                fields['html'] = message.html
            
            reply_to = self._get_reply_to(message)
            if reply_to:
                fields['h:Reply-To'] = reply_to
            
            for key, value in fields.items():
                parts.append(
                    f'--{boundary}\r\n'
                    f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
                    f'{value}'
                )
            
            # Add attachments
            for attachment in message.attachments:
                encoded_content = attachment.get_base64()
                parts.append(
                    f'--{boundary}\r\n'
                    f'Content-Disposition: form-data; name="attachment"; filename="{attachment.filename}"\r\n'
                    f'Content-Type: {attachment.content_type}\r\n'
                    f'Content-Transfer-Encoding: base64\r\n\r\n'
                    f'{encoded_content}'
                )
            
            # Close boundary
            parts.append(f'--{boundary}--\r\n')
            
            body = '\r\n'.join(parts).encode('utf-8')
            
            # Create request
            credentials = base64.b64encode(f'api:{self._api_key}'.encode()).decode()
            headers = {
                'Authorization': f'Basic {credentials}',
                'Content-Type': f'multipart/form-data; boundary={boundary}'
            }
            
            req = urllib.request.Request(url, data=body, headers=headers, method='POST')
            
            with urllib.request.urlopen(req, timeout=self.config.timeout) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                
                return EmailResponse.success_response(
                    message_id=response_data.get('id', ''),
                    provider=self.name,
                    recipients=message.get_all_recipients(),
                    raw_response=response_data
                )
        
        except Exception as e:
            return EmailResponse.failure_response(
                error=f"Mailgun error with attachments: {e}",
                provider=self.name,
                recipients=message.get_all_recipients()
            )
