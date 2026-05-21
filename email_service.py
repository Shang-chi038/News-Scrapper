import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

class EmailService:
    """Service for sending email digests"""
    
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def send_digest(self, recipients: List[str], subject: str, html_content: str, text_content: str = None):
        """Send email digest to recipients"""
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = ', '.join(recipients)
            
            # Add plain text version (fallback)
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                message.attach(text_part)
            
            # Add HTML version
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)
            
            # Connect and send
            print(f"Connecting to {self.smtp_server}:{self.smtp_port}...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"✅ Email sent successfully to {len(recipients)} recipient(s)")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
