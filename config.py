import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration settings for the news scraper system"""
    
    # Email settings
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    EMAIL_SENDER = os.getenv('EMAIL_SENDER', 'your-email@gmail.com')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your-app-password')
    EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', 'recipient@example.com').split(',')
    
    # Scraping settings
    REQUEST_TIMEOUT = 10
    MAX_RETRIES = 3
    
    # Digest settings
    DIGEST_TITLE = "Daily News Digest"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is set"""
        if cls.EMAIL_SENDER == 'your-email@gmail.com':
            print("Warning: EMAIL_SENDER not configured")
            return False
        if cls.EMAIL_PASSWORD == 'your-app-password':
            print("Warning: EMAIL_PASSWORD not configured")
            return False
        return True
