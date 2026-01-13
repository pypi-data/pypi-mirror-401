"""
SendGrid email provider.

This module implements the SendGrid email provider for sending emails
through the SendGrid API.
"""

import json
from typing import Optional, Dict, Any
import base64

from .base import BaseEmailProvider
from ..config import EmailConfig
from ..message import EmailMessage
from ..response import EmailResponse
from ..exceptions import ProviderError, AuthenticationError


class SendGridProvider(BaseEmailProvider):
    """
    SendGrid email provider.
    
    Sends emails through SendGrid's Web API v3.
    """
    
    API_BASE_URL = 'https://api.sendgrid.com/v3'
    
    def __init__(self, config: EmailConfig):
        """
        Initialize SendGrid provider.
        
        Args:
            config: Email configuration with SendGrid settings
        """
        super().__init__(config)
        self._api_key = config.sendgrid.api_key
        self._sandbox_mode = config.sendgrid.sandbox_mode
    
    @property
    def name(self) -> str:
        return 'sendgrid'
    
    def send(self, message: EmailMessage) -> EmailResponse:
        """
        Send an email via SendGrid API.
        
        Args:
            message: Email message to send
        
        Returns:
            EmailResponse with send result
        """
        try:
            # Try to import sendgrid library
            try:
                from sendgrid import SendGridAPIClient
                from sendgrid.helpers.mail import (
                    Mail, From, To, Cc, Bcc, Subject, Content,
                    Attachment as SGAttachment, FileName, FileContent,
                    FileType, Disposition, ContentId
                )
            except ImportError:
                # Fallback to HTTP request
                return self._send_via_http(message)
            
            # Build SendGrid mail object
            mail = Mail()
            
            # Set from address
            from_email = self._get_from_address(message)
            mail.from_email = From(from_email)
            
            # Set recipients
            for recipient in message.to:
                mail.add_to(To(recipient))
            
            if message.cc:
                for cc in message.cc:
                    mail.add_cc(Cc(cc))
            
            if message.bcc:
                for bcc in message.bcc:
                    mail.add_bcc(Bcc(bcc))
            
            # Set subject
            mail.subject = Subject(message.subject)
            
            # Set content
            if message.text:
                mail.add_content(Content('text/plain', message.text))
            
            if message.html:
                mail.add_content(Content('text/html', message.html))
            
            # Set reply-to
            reply_to = self._get_reply_to(message)
            if reply_to:
                from sendgrid.helpers.mail import ReplyTo
                mail.reply_to = ReplyTo(reply_to)
            
            # Add attachments
            for attachment in message.attachments:
                sg_attachment = SGAttachment()
                sg_attachment.file_content = FileContent(attachment.get_base64())
                sg_attachment.file_name = FileName(attachment.filename)
                sg_attachment.file_type = FileType(attachment.content_type)
                
                if attachment.is_inline:
                    sg_attachment.disposition = Disposition('inline')
                    if attachment.content_id:
                        sg_attachment.content_id = ContentId(attachment.content_id)
                else:
                    sg_attachment.disposition = Disposition('attachment')
                
                mail.add_attachment(sg_attachment)
            
            # Add custom headers
            if message.headers:
                from sendgrid.helpers.mail import Header
                for key, value in message.headers.items():
                    mail.add_header(Header(key, value))
            
            # Add categories/tags
            if message.tags:
                from sendgrid.helpers.mail import Category
                for tag in message.tags:
                    mail.add_category(Category(tag))
            
            # Enable sandbox mode if configured
            if self._sandbox_mode:
                from sendgrid.helpers.mail import MailSettings, SandBoxMode
                mail.mail_settings = MailSettings()
                mail.mail_settings.sandbox_mode = SandBoxMode(True)
            
            # Send email
            sg = SendGridAPIClient(self._api_key)
            response = sg.send(mail)
            
            if response.status_code in (200, 201, 202):
                # Extract message ID from headers
                message_id = response.headers.get('X-Message-Id', '')
                
                return EmailResponse.success_response(
                    message_id=message_id,
                    provider=self.name,
                    recipients=message.get_all_recipients(),
                    raw_response={
                        'status_code': response.status_code,
                        'headers': dict(response.headers)
                    }
                )
            else:
                return EmailResponse.failure_response(
                    error=f"SendGrid returned status {response.status_code}",
                    provider=self.name,
                    error_code=str(response.status_code),
                    recipients=message.get_all_recipients()
                )
        
        except Exception as e:
            return EmailResponse.failure_response(
                error=f"SendGrid error: {e}",
                provider=self.name,
                recipients=message.get_all_recipients()
            )
    
    def _send_via_http(self, message: EmailMessage) -> EmailResponse:
        """
        Send email using HTTP requests (fallback when sendgrid library not installed).
        
        Args:
            message: Email message to send
        
        Returns:
            EmailResponse with send result
        """
        try:
            import urllib.request
            import urllib.error
            
            url = f"{self.API_BASE_URL}/mail/send"
            
            # Build request payload
            payload = self._build_api_payload(message)
            
            # Create request
            headers = {
                'Authorization': f'Bearer {self._api_key}',
                'Content-Type': 'application/json'
            }
            
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')
            
            # Send request
            with urllib.request.urlopen(req, timeout=self.config.timeout) as response:
                status_code = response.getcode()
                response_headers = dict(response.getheaders())
                
                if status_code in (200, 201, 202):
                    message_id = response_headers.get('X-Message-Id', '')
                    
                    return EmailResponse.success_response(
                        message_id=message_id,
                        provider=self.name,
                        recipients=message.get_all_recipients()
                    )
                else:
                    return EmailResponse.failure_response(
                        error=f"SendGrid returned status {status_code}",
                        provider=self.name,
                        error_code=str(status_code)
                    )
        
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ''
            return EmailResponse.failure_response(
                error=f"SendGrid API error: {e.code} - {error_body}",
                provider=self.name,
                error_code=str(e.code)
            )
        except Exception as e:
            return EmailResponse.failure_response(
                error=f"SendGrid error: {e}",
                provider=self.name
            )
    
    def _build_api_payload(self, message: EmailMessage) -> Dict[str, Any]:
        """Build SendGrid API payload from EmailMessage."""
        payload = {
            'personalizations': [{
                'to': [{'email': email} for email in message.to]
            }],
            'from': {'email': self._get_from_address(message)},
            'subject': message.subject,
            'content': []
        }
        
        # Add CC and BCC
        if message.cc:
            payload['personalizations'][0]['cc'] = [{'email': cc} for cc in message.cc]
        
        if message.bcc:
            payload['personalizations'][0]['bcc'] = [{'email': bcc} for bcc in message.bcc]
        
        # Add content
        if message.text:
            payload['content'].append({
                'type': 'text/plain',
                'value': message.text
            })
        
        if message.html:
            payload['content'].append({
                'type': 'text/html',
                'value': message.html
            })
        
        # Add reply-to
        reply_to = self._get_reply_to(message)
        if reply_to:
            payload['reply_to'] = {'email': reply_to}
        
        # Add attachments
        if message.attachments:
            payload['attachments'] = []
            for attachment in message.attachments:
                att_data = {
                    'content': attachment.get_base64(),
                    'filename': attachment.filename,
                    'type': attachment.content_type,
                    'disposition': 'inline' if attachment.is_inline else 'attachment'
                }
                if attachment.content_id:
                    att_data['content_id'] = attachment.content_id
                payload['attachments'].append(att_data)
        
        # Add sandbox mode
        if self._sandbox_mode:
            payload['mail_settings'] = {'sandbox_mode': {'enable': True}}
        
        # Add categories/tags
        if message.tags:
            payload['categories'] = message.tags
        
        return payload
