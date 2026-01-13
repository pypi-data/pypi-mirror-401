"""
SMTP email provider.

This module implements the SMTP email provider for sending emails
through any SMTP server.
"""

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr, formatdate, make_msgid
from typing import Optional
import uuid

from .base import BaseEmailProvider
from ..config import EmailConfig, SMTPConfig
from ..message import EmailMessage
from ..response import EmailResponse
from ..exceptions import ConnectionError, AuthenticationError, ProviderError


class SMTPProvider(BaseEmailProvider):
    """
    SMTP email provider.
    
    Sends emails through SMTP servers using Python's smtplib.
    """
    
    def __init__(self, config: EmailConfig, smtp_config: Optional[SMTPConfig] = None):
        """
        Initialize SMTP provider.
        
        Args:
            config: Main email configuration
            smtp_config: Optional SMTP-specific configuration override
        """
        super().__init__(config)
        self._smtp_config = smtp_config or config.smtp
        self._connection: Optional[smtplib.SMTP] = None
    
    @property
    def name(self) -> str:
        return 'smtp'
    
    def connect(self) -> None:
        """Establish connection to SMTP server."""
        if self._connection:
            return
        
        try:
            if self._smtp_config.use_ssl:
                # Use SSL from the start
                context = ssl.create_default_context()
                self._connection = smtplib.SMTP_SSL(
                    self._smtp_config.host,
                    self._smtp_config.port,
                    timeout=self._smtp_config.timeout,
                    context=context
                )
            else:
                # Regular SMTP with optional STARTTLS
                self._connection = smtplib.SMTP(
                    self._smtp_config.host,
                    self._smtp_config.port,
                    timeout=self._smtp_config.timeout,
                    local_hostname=self._smtp_config.local_hostname
                )
                
                if self._smtp_config.use_tls:
                    context = ssl.create_default_context()
                    self._connection.starttls(context=context)
            
            # Authenticate if credentials provided
            if self._smtp_config.username and self._smtp_config.password:
                try:
                    self._connection.login(
                        self._smtp_config.username,
                        self._smtp_config.password
                    )
                except smtplib.SMTPAuthenticationError as e:
                    raise AuthenticationError(
                        f"SMTP authentication failed: {e}",
                        provider=self.name
                    )
        
        except smtplib.SMTPConnectError as e:
            raise ConnectionError(
                f"Failed to connect to SMTP server: {e}",
                host=self._smtp_config.host,
                port=self._smtp_config.port
            )
        except Exception as e:
            raise ConnectionError(
                f"SMTP connection error: {e}",
                host=self._smtp_config.host,
                port=self._smtp_config.port
            )
    
    def disconnect(self) -> None:
        """Close SMTP connection."""
        if self._connection:
            try:
                self._connection.quit()
            except Exception:
                pass
            finally:
                self._connection = None
    
    def send(self, message: EmailMessage) -> EmailResponse:
        """
        Send an email via SMTP.
        
        Args:
            message: Email message to send
        
        Returns:
            EmailResponse with send result
        """
        try:
            # Ensure connection
            if not self._connection:
                self.connect()
            
            # Build MIME message
            mime_msg = self._build_mime_message(message)
            
            # Get from address
            from_addr = self._get_from_address(message)
            
            # Get all recipients
            recipients = message.get_all_recipients()
            
            # Send email
            self._connection.sendmail(
                from_addr,
                recipients,
                mime_msg.as_string()
            )
            
            # Generate message ID
            message_id = mime_msg['Message-ID'] or str(uuid.uuid4())
            
            return EmailResponse.success_response(
                message_id=message_id,
                provider=self.name,
                recipients=recipients
            )
        
        except smtplib.SMTPException as e:
            return EmailResponse.failure_response(
                error=f"SMTP error: {e}",
                provider=self.name,
                recipients=message.get_all_recipients()
            )
        except Exception as e:
            return EmailResponse.failure_response(
                error=f"Failed to send email: {e}",
                provider=self.name,
                recipients=message.get_all_recipients()
            )
    
    def _build_mime_message(self, message: EmailMessage) -> MIMEMultipart:
        """
        Build a MIME message from EmailMessage.
        
        Args:
            message: Email message
        
        Returns:
            MIMEMultipart message
        """
        # Create multipart message
        if message.attachments:
            mime_msg = MIMEMultipart('mixed')
            msg_alternative = MIMEMultipart('alternative')
            mime_msg.attach(msg_alternative)
        else:
            mime_msg = MIMEMultipart('alternative')
            msg_alternative = mime_msg
        
        # Set headers
        from_addr = self._get_from_address(message)
        mime_msg['From'] = from_addr
        mime_msg['To'] = ', '.join(message.to)
        mime_msg['Subject'] = message.subject
        mime_msg['Date'] = formatdate(localtime=True)
        mime_msg['Message-ID'] = make_msgid()
        
        if message.cc:
            mime_msg['Cc'] = ', '.join(message.cc)
        
        reply_to = self._get_reply_to(message)
        if reply_to:
            mime_msg['Reply-To'] = reply_to
        
        # Add custom headers
        for key, value in message.headers.items():
            mime_msg[key] = value
        
        # Add text body
        if message.text:
            text_part = MIMEText(message.text, 'plain', 'utf-8')
            msg_alternative.attach(text_part)
        
        # Add HTML body
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
                part.add_header(
                    'Content-Disposition',
                    'inline',
                    filename=attachment.filename
                )
            else:
                part.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=attachment.filename
                )
            
            if attachment.content_type:
                part.replace_header('Content-Type', attachment.content_type)
            
            mime_msg.attach(part)
        
        return mime_msg
