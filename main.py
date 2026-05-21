<<<<<<< HEAD
from datetime import datetime

def main():
    """Main entry point for the news scraper system"""
    
    print("=" * 60)
    print("NEWS SCRAPER SYSTEM")
    print("=" * 60)
    print(f"Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Initialize scrapers
    from scrapers.channels import ChannelsNewsScraper
    from scrapers.techcrunch import TechCrunchScraper
    from scrapers.hackernews import HackerNewsScraper
    
    scrapers = [
        ChannelsNewsScraper(),
        TechCrunchScraper(),
        HackerNewsScraper()
    ]
    
    # Initialize aggregator
    from aggregator import NewsAggregator
    aggregator = NewsAggregator(scrapers)
    
    # Generate digests
    print("\n📊 Generating digests...\n")
    text_digest = aggregator.generate_text_digest()
    html_digest = aggregator.generate_html_digest()
    
    # Save to file
    aggregator.save_to_json('daily_news.json')
    
    # Print text version
    print("\n" + text_digest)
    
    # Send email
    from config import Config
    from email_service import EmailService
    
    if Config.validate():
        print("\n📧 Sending email digest...\n")
        email_service = EmailService(
            smtp_server=Config.SMTP_SERVER,
            smtp_port=Config.SMTP_PORT,
            sender_email=Config.EMAIL_SENDER,
            sender_password=Config.EMAIL_PASSWORD
        )
        
        subject = f"{Config.DIGEST_TITLE} - {datetime.now().strftime('%B %d, %Y')}"
        email_service.send_digest(
            recipients=Config.EMAIL_RECIPIENTS,
            subject=subject,
            html_content=html_digest,
            text_content=text_digest
        )
    else:
        print("\n⚠️  Email not configured. Set environment variables:")
        print("   - EMAIL_SENDER")
        print("   - EMAIL_PASSWORD")
        print("   - EMAIL_RECIPIENTS (comma-separated)")
        print("\nDigest has been generated and saved locally.")
    
    print("\n" + "=" * 60)
    print("COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()
=======
from datetime import datetime

def main():
    """Main entry point for the news scraper system"""
    
    print("=" * 60)
    print("NEWS SCRAPER SYSTEM")
    print("=" * 60)
    print(f"Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Initialize scrapers
    from scrapers.channels import ChannelsNewsScraper
    from scrapers.techcrunch import TechCrunchScraper
    from scrapers.hackernews import HackerNewsScraper
    
    scrapers = [
        ChannelsNewsScraper(),
        TechCrunchScraper(),
        HackerNewsScraper()
    ]
    
    # Initialize aggregator
    from aggregator import NewsAggregator
    aggregator = NewsAggregator(scrapers)
    
    # Generate digests
    print("\n📊 Generating digests...\n")
    text_digest = aggregator.generate_text_digest()
    html_digest = aggregator.generate_html_digest()
    
    # Save to file
    aggregator.save_to_json('daily_news.json')
    
    # Print text version
    print("\n" + text_digest)
    
    # Send email
    from config import Config
    from email_service import EmailService
    
    if Config.validate():
        print("\n📧 Sending email digest...\n")
        email_service = EmailService(
            smtp_server=Config.SMTP_SERVER,
            smtp_port=Config.SMTP_PORT,
            sender_email=Config.EMAIL_SENDER,
            sender_password=Config.EMAIL_PASSWORD
        )
        
        subject = f"{Config.DIGEST_TITLE} - {datetime.now().strftime('%B %d, %Y')}"
        email_service.send_digest(
            recipients=Config.EMAIL_RECIPIENTS,
            subject=subject,
            html_content=html_digest,
            text_content=text_digest
        )
    else:
        print("\n⚠️  Email not configured. Set environment variables:")
        print("   - EMAIL_SENDER")
        print("   - EMAIL_PASSWORD")
        print("   - EMAIL_RECIPIENTS (comma-separated)")
        print("\nDigest has been generated and saved locally.")
    
    print("\n" + "=" * 60)
    print("COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()
>>>>>>> 8aefad5 (I included test files so that I can move all my)
